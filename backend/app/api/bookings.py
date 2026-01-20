from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, time, datetime, timedelta

from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.crud.booking import create_booking, get_bookings_by_date, is_slot_taken

router = APIRouter(tags=["Bookings"])


@router.post("/book", response_model=BookingResponse, status_code=201)
def book(payload: BookingCreate, db: Session = Depends(get_db)):
    # Conflict check
    if is_slot_taken(db, payload.date, payload.time):
        raise HTTPException(status_code=409, detail="This slot is already booked")

    return create_booking(db, payload)


@router.get("/slots")
def get_slots(
    day: date = Query(..., alias="date"),
    db: Session = Depends(get_db),
):
    """
    MVP: working hours 09:00 -> 17:00, every 30 minutes.
    Returns available slots only.
    """
    # Generate all slots
    start = datetime.combine(day, time(9, 0))
    end = datetime.combine(day, time(17, 0))
    step = timedelta(minutes=30)

    all_slots = []
    cur = start
    while cur < end:
        all_slots.append(cur.time())
        cur += step

    # Remove booked slots
    booked = {b.time for b in get_bookings_by_date(db, day)}
    available = [s.strftime("%H:%M") for s in all_slots if s not in booked]

    return {"date": str(day), "available_slots": available}
