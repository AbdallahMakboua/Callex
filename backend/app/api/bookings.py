import logging
from datetime import datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse, SlotsResponse, SlotItem
from app.crud.booking import create_booking, get_bookings_by_date, is_slot_taken

router = APIRouter(tags=["Bookings"])

# Use Uvicorn logger so logs always show in Docker output
logger = logging.getLogger("uvicorn.error")

WORK_START = time(9, 0)
WORK_END = time(17, 0)
SLOT_MINUTES = 30


@router.post("/book", response_model=BookingResponse, status_code=201)
def book(payload: BookingCreate, db: Session = Depends(get_db)):
    # Conflict check
    if is_slot_taken(db, payload.date, payload.time):
        logger.info("booking_conflict date=%s time=%s", payload.date, payload.time)
        raise HTTPException(status_code=409, detail="This slot is already booked")

    booking = create_booking(db, payload)
    logger.info(
        "booking_created id=%s date=%s time=%s",
        booking.id,
        booking.date,
        booking.time,
    )
    return booking


@router.get("/slots", response_model=SlotsResponse)
def get_slots(
    date: str = Query(..., description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    try:
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    booked_times = {b.time.strftime("%H:%M") for b in get_bookings_by_date(db, booking_date)}

    slots = []
    current = datetime.combine(booking_date, WORK_START)
    end = datetime.combine(booking_date, WORK_END)

    while current < end:
        t = current.strftime("%H:%M")
        slots.append(SlotItem(time=t, available=t not in booked_times))
        current += timedelta(minutes=SLOT_MINUTES)

    logger.info("slots_checked date=%s", date)

    return SlotsResponse(
        date=date,
        slot_duration_minutes=SLOT_MINUTES,
        working_hours={
            "from": WORK_START.strftime("%H:%M"),
            "to": WORK_END.strftime("%H:%M"),
        },
        slots=slots,
    )
