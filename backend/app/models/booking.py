from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, UniqueConstraint
from app.db.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Unique constraint: prevent double booking for same date+time
    __table_args__ = (
        UniqueConstraint("date", "time", name="uq_date_time"),
    )
