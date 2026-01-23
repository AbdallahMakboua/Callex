from __future__ import annotations

from datetime import datetime, time
from typing import Literal

Preference = Literal["morning", "afternoon", "evening", "any"]


def _bucket_for(t: time) -> Preference:
    if time(9, 0) <= t < time(12, 0):
        return "morning"
    if time(12, 0) <= t < time(15, 0):
        return "afternoon"
    if time(15, 0) <= t < time(17, 0):
        return "evening"
    return "any"


def filter_available_slots(
    slots_payload: dict,
    preference: Preference = "any",
) -> dict:
    """
    slots_payload expected to match /slots structured response.
    Returns same structure but with only available slots, optionally filtered by preference.
    """
    filtered = []
    for s in slots_payload.get("slots", []):
        if not s.get("available"):
            continue
        t = datetime.strptime(s["time"], "%H:%M").time()
        bucket = _bucket_for(t)
        if preference != "any" and bucket != preference:
            continue
        filtered.append(s["time"])

    return {
        "date": slots_payload.get("date"),
        "preference": preference,
        "available_slots": filtered,
        "count": len(filtered),
    }
