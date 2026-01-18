from datetime import date, time, datetime
from pydantic import BaseModel


class BookingCreate(BaseModel):
    """Schema for creating a booking."""
    name: str
    phone: str
    date: date
    time: time


class BookingResponse(BaseModel):
    """Schema for returning a booking."""
    id: int
    name: str
    phone: str
    date: date
    time: time
    created_at: datetime

    class Config:
        from_attributes = True
