from datetime import date as dt_date  # Use alias to avoid name clashes
from sqlalchemy import select  # SQLAlchemy query builder
from sqlalchemy.orm import Session  # SQLAlchemy session type
from sqlalchemy.exc import IntegrityError  # Raised on DB constraint violations (e.g., UNIQUE)

from app.models.booking import Booking  # SQLAlchemy model
from app.schemas.booking import BookingCreate  # Input schema used by API layer


def create_booking(db: Session, data: BookingCreate) -> Booking:
    """
    Insert a booking row into the database.

    IMPORTANT:
    - With DB UNIQUE constraint on (date, time), concurrent requests can raise IntegrityError.
    - We rollback and re-raise so the API layer can convert it to HTTP 409.
    """
    # Build ORM object from validated request payload
    booking = Booking(
        name=data.name,
        phone=data.phone,
        date=data.date,
        time=data.time,
    )

    # Stage object for insert
    db.add(booking)

    try:
        # Commit transaction (this is where UNIQUE violations can happen)
        db.commit()
    except IntegrityError:
        # Always rollback the session after a failed commit
        db.rollback()
        # Re-raise so API can return a clean 409 Conflict
        raise

    # Reload generated fields (id, created_at, etc.)
    db.refresh(booking)
    return booking


def get_bookings_by_date(db: Session, day: dt_date) -> list[Booking]:
    """
    Return all bookings for the given date ordered by time.
    """
    stmt = select(Booking).where(Booking.date == day).order_by(Booking.time.asc())
    return list(db.execute(stmt).scalars().all())


def is_slot_taken(db: Session, day: dt_date, t) -> bool:
    """
    Fast existence check: returns True if date+time exists.
    """
    stmt = select(Booking).where(Booking.date == day, Booking.time == t)
    return db.execute(stmt).scalar_one_or_none() is not None
