import logging  # Standard Python logging
from datetime import datetime, time, timedelta  # Date/time utilities for slot generation

from fastapi import APIRouter, Depends, HTTPException, Query  # FastAPI components
from sqlalchemy.orm import Session  # DB session type
from sqlalchemy.exc import IntegrityError  # Raised on DB constraint violations

from app.db.database import get_db  # Dependency that provides a DB session
from app.schemas.booking import BookingCreate, BookingResponse, SlotsResponse, SlotItem  # API schemas
from app.crud.booking import create_booking, get_bookings_by_date, is_slot_taken  # DB operations
from app.ai.availability import filter_available_slots  # Filter availability by preference buckets
from app.schemas.ai import AIBookRequest, AIBookSuggestResponse, AIBookConfirmedResponse  # AI endpoint schemas
from app.ai.booking_flow import normalize_time, validate_date, nearest_slots  # Helpers for AI booking flow

router = APIRouter(tags=["Bookings"])  # Router group for booking endpoints

# Use Uvicorn logger so messages appear in Docker logs reliably
logger = logging.getLogger("uvicorn.error")

# Default working hours and slot duration (MVP defaults)
WORK_START = time(9, 0)   # Day starts at 09:00
WORK_END = time(17, 0)    # Day ends at 17:00
SLOT_MINUTES = 30         # Each slot is 30 minutes


@router.post("/book", response_model=BookingResponse, status_code=201)
def book(payload: BookingCreate, db: Session = Depends(get_db)):
    """
    Create a booking (strict API behavior).
    - Returns 201 if created
    - Returns 409 if slot already booked
    """

    # API-level conflict check (fast path)
    if is_slot_taken(db, payload.date, payload.time):
        logger.info("booking_conflict date=%s time=%s", payload.date, payload.time)
        raise HTTPException(status_code=409, detail="This slot is already booked")

    # Insert booking into DB (DB-level uniqueness may still fail under concurrency)
    try:
        booking = create_booking(db, payload)
    except IntegrityError:
        # Convert DB UNIQUE violation to HTTP 409 instead of 500
        logger.info("booking_conflict_db date=%s time=%s", payload.date, payload.time)
        raise HTTPException(status_code=409, detail="This slot is already booked")

    # Log business event
    logger.info("booking_created id=%s date=%s time=%s", booking.id, booking.date, booking.time)

    return booking


@router.get("/slots", response_model=SlotsResponse)
def get_slots(date: str = Query(..., description="YYYY-MM-DD"), db: Session = Depends(get_db)):
    """
    Return all time slots for a given date with availability boolean.
    """

    # Validate date format
    try:
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Collect booked times as "HH:MM" for quick availability checks
    booked_times = {b.time.strftime("%H:%M") for b in get_bookings_by_date(db, booking_date)}

    # Generate all slots for the day
    slots: list[SlotItem] = []
    current = datetime.combine(booking_date, WORK_START)
    end = datetime.combine(booking_date, WORK_END)

    while current < end:
        t = current.strftime("%H:%M")
        slots.append(SlotItem(time=t, available=(t not in booked_times)))
        current += timedelta(minutes=SLOT_MINUTES)

    logger.info("slots_checked date=%s", date)

    return SlotsResponse(
        date=date,
        slot_duration_minutes=SLOT_MINUTES,
        working_hours={"from": WORK_START.strftime("%H:%M"), "to": WORK_END.strftime("%H:%M")},
        slots=slots,
    )


@router.get("/ai/availability")
def ai_availability(
    date: str = Query(..., description="YYYY-MM-DD"),
    preference: str = Query("any", description="any|morning|afternoon|evening"),
    db: Session = Depends(get_db),
):
    """
    AI helper endpoint:
    - Returns available slots filtered by preference bucket (morning/afternoon/evening/any)
    """

    # Validate preference value
    if preference not in {"any", "morning", "afternoon", "evening"}:
        raise HTTPException(status_code=400, detail="Invalid preference")

    # Validate date format
    try:
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Build set of booked times (as "HH:MM")
    booked_times = {b.time.strftime("%H:%M") for b in get_bookings_by_date(db, booking_date)}

    # Generate slot list in dict form expected by filter_available_slots()
    slots = []
    current = datetime.combine(booking_date, WORK_START)
    end = datetime.combine(booking_date, WORK_END)

    while current < end:
        t = current.strftime("%H:%M")
        slots.append({"time": t, "available": (t not in booked_times)})
        current += timedelta(minutes=SLOT_MINUTES)

    slots_payload = {
        "date": date,
        "slot_duration_minutes": SLOT_MINUTES,
        "working_hours": {"from": WORK_START.strftime("%H:%M"), "to": WORK_END.strftime("%H:%M")},
        "slots": slots,
    }

    result = filter_available_slots(slots_payload, preference=preference)

    logger.info("ai_availability date=%s preference=%s count=%s", date, preference, result.get("count"))
    return result


@router.post("/ai/book")
def ai_book(payload: AIBookRequest, db: Session = Depends(get_db)):
    """
    Smarter AI booking flow:
    - If time is missing -> return ALL available slots (filtered by preference)
    - If time is provided but unavailable -> suggest 2 nearest available slots
    - If time is available -> create booking
    """

    # Validate date format early
    try:
        validate_date(payload.date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    # Validate preference early
    if payload.preference not in {"any", "morning", "afternoon", "evening"}:
        raise HTTPException(status_code=400, detail="Invalid preference")

    # Convert date string into a Python date object
    booking_date = datetime.strptime(payload.date, "%Y-%m-%d").date()

    # Collect booked times as "HH:MM"
    booked_times = {b.time.strftime("%H:%M") for b in get_bookings_by_date(db, booking_date)}

    # Build day slots payload for filtering
    slots = []
    current = datetime.combine(booking_date, WORK_START)
    end = datetime.combine(booking_date, WORK_END)

    while current < end:
        t = current.strftime("%H:%M")
        slots.append({"time": t, "available": (t not in booked_times)})
        current += timedelta(minutes=SLOT_MINUTES)

    slots_payload = {
        "date": payload.date,
        "slot_duration_minutes": SLOT_MINUTES,
        "working_hours": {"from": WORK_START.strftime("%H:%M"), "to": WORK_END.strftime("%H:%M")},
        "slots": slots,
    }

    # CASE A: No time provided -> return ALL available slots for the requested preference
    if payload.time is None:
        availability = filter_available_slots(slots_payload, preference=payload.preference)
        suggestions = availability.get("available_slots", [])

        msg = "Available slots:" if suggestions else "No available slots for this date."
        logger.info("ai_book_suggest_all date=%s pref=%s count=%s", payload.date, payload.preference, len(suggestions))

        return AIBookSuggestResponse(
            action="suggest",
            date=payload.date,
            preference=payload.preference,
            requested_time=None,
            reason=None,
            suggestions=suggestions,
            message=msg,
        )

    # CASE B/C: Time provided -> normalize to "HH:MM"
    try:
        chosen_time = normalize_time(payload.time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format (use HH:MM or HH:MM:SS)")

    # Build full available list for nearest suggestions (use preference="any" for best UX)
    all_available = filter_available_slots(slots_payload, preference="any").get("available_slots", [])

    # CASE B: Time is not available -> suggest 2 nearest available times
    if chosen_time not in all_available:
        closest = nearest_slots(all_available, chosen_time, k=2) if all_available else []
        msg = (
            f"{chosen_time} is not available. Closest available slots: {', '.join(closest)}"
            if closest
            else "No available slots for this date."
        )

        logger.info("ai_book_time_unavailable date=%s requested=%s", payload.date, chosen_time)

        return AIBookSuggestResponse(
            action="suggest",
            date=payload.date,
            preference=payload.preference,
            requested_time=chosen_time,
            reason="requested_time_unavailable",
            suggestions=closest,
            message=msg,
        )

    # CASE C: Time is available -> attempt to book
    from datetime import time as dt_time
    from app.schemas.booking import BookingCreate as BookingCreateSchema

    booking_create = BookingCreateSchema(
        name=payload.name,
        phone=payload.phone,
        date=booking_date,
        time=dt_time.fromisoformat(chosen_time + ":00"),
    )

    # Optional API-level check (fast path). DB-level check still protects concurrency.
    if is_slot_taken(db, booking_create.date, booking_create.time):
        logger.info("ai_book_conflict date=%s time=%s", payload.date, chosen_time)
        raise HTTPException(status_code=409, detail="This slot is already booked")

    # Insert booking; convert DB UNIQUE violation into HTTP 409
    try:
        booking = create_booking(db, booking_create)
    except IntegrityError:
        logger.info("ai_book_conflict_db date=%s time=%s", payload.date, chosen_time)
        raise HTTPException(status_code=409, detail="This slot is already booked")

    logger.info("ai_book_created id=%s date=%s time=%s", booking.id, payload.date, chosen_time)

    return AIBookConfirmedResponse(
        action="booked",
        message="Booking confirmed.",
        booking={
            "id": booking.id,
            "name": booking.name,
            "phone": booking.phone,
            "date": str(booking.date),
            "time": booking.time.strftime("%H:%M:%S"),
            "created_at": str(booking.created_at),
        },
    )
