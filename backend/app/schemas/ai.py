from pydantic import BaseModel
from typing import Literal, Optional, List

Preference = Literal["any", "morning", "afternoon", "evening"]

class AIBookRequest(BaseModel):
    name: str
    phone: str
    date: str  # YYYY-MM-DD
    preference: Preference = "any"
    time: Optional[str] = None  # HH:MM or HH:MM:SS

class AIBookSuggestResponse(BaseModel):
    action: Literal["suggest"]
    date: str
    preference: Preference
    requested_time: Optional[str] = None
    reason: Optional[str] = None  # e.g. "requested_time_unavailable"
    suggestions: List[str]
    message: str

class AIBookConfirmedResponse(BaseModel):
    action: Literal["booked"]
    message: str
    booking: dict
