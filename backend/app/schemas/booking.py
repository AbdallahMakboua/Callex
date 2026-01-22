from pydantic import BaseModel
from datetime import date, time, datetime
from typing import List, Dict


class BookingCreate(BaseModel):
    name: str
    phone: str
    date: date
    time: time


class BookingResponse(BaseModel):
    id: int
    name: str
    phone: str
    date: date
    time: time
    created_at: datetime

    class Config:
        from_attributes = True


class SlotItem(BaseModel):
    time: str
    available: bool


class SlotsResponse(BaseModel):
    date: str
    slot_duration_minutes: int
    working_hours: Dict[str, str]
    slots: List[SlotItem]
