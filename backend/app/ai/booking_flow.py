from datetime import datetime
from typing import Optional, List

from app.ai.availability import filter_available_slots

def top_suggestions(payload: dict, preference: str, limit: int = 5) -> List[str]:
    result = filter_available_slots(payload, preference=preference)  # returns available_slots list
    slots = result.get("available_slots", [])
    return slots[:limit]

def normalize_time(t: str) -> str:
    # Accept HH:MM or HH:MM:SS and normalize to HH:MM
    if len(t) == 5:
        return t
    if len(t) >= 8:
        return t[:5]
    raise ValueError("Invalid time format")

def validate_date(date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format")

def nearest_slots(available_times: list[str], requested: str, k: int = 2) -> list[str]:
    req = datetime.strptime(requested, "%H:%M")
    scored = []
    for t in available_times:
        tt = datetime.strptime(t, "%H:%M")
        scored.append((abs((tt - req).total_seconds()), t))
    scored.sort(key=lambda x: x[0])
    return [t for _, t in scored[:k]]
