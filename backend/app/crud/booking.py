from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date as dt_date

from app.models.booking import Booking
from app.schemas.booking import BookingCreate

from datetime import date
from backend.app.models.booking import Booking


def create_booking(db: Session, data: BookingCreate) -> Booking:
    booking = Booking(
        name=data.name,
        phone=data.phone,
        date=data.date,
        time=data.time,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_bookings_by_date(db: Session, day: dt_date) -> list[Booking]:
    stmt = select(Booking).where(Booking.date == day).order_by(Booking.time.asc())
    return list(db.execute(stmt).scalars().all())


def is_slot_taken(db: Session, day: dt_date, t) -> bool:
    stmt = select(Booking).where(Booking.date == day, Booking.time == t)
    return db.execute(stmt).scalar_one_or_none() is not None


def get_booked_times_by_date(db: Session, booking_date: date):
    """
    Returns list of booked times as HH:MM strings
    """
    rows = (
        db.query(Booking.time)
        .filter(Booking.date == booking_date)
        .all()
    )
    return [r[0].strftime("%H:%M") for r in rows]
