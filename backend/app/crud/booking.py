from datetime import date as dt_date
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.schemas.booking import BookingCreate


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
