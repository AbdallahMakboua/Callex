# Callex API Documentation

Base URL (local):
```
http://localhost:8000
```

## Conventions

- Dates use `YYYY-MM-DD`
- Times use `HH:MM` (recommended) or `HH:MM:SS`
- Working hours default: **09:00 → 17:00**
- Slot duration default: **30 minutes**
- Timezone: **local** (host/container local time)

---

## GET /health

Simple health check.

### Endpoint
```
GET /health
```

### Example
```bash
curl http://localhost:8000/health
```

### Response — 200
```json
{"status":"ok"}
```

---

## GET /slots

Return all slots for a given date with an `available` boolean.

### Endpoint
```
GET /slots?date=YYYY-MM-DD
```

### Query Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| date | string | yes | Date in format `YYYY-MM-DD` |

### Business Rules
- Working hours: **09:00 → 17:00**
- Slot duration: **30 minutes**
- Booked slots are marked as `"available": false`

### Example Request
```bash
curl "http://localhost:8000/slots?date=2026-01-20"
```

### Example Response — 200
```json
{
  "date": "2026-01-20",
  "slot_duration_minutes": 30,
  "working_hours": {
    "from": "09:00",
    "to": "17:00"
  },
  "slots": [
    { "time": "09:00", "available": true },
    { "time": "09:30", "available": true },
    { "time": "10:00", "available": false },
    { "time": "10:30", "available": true }
  ]
}
```

### Error Responses

#### 400 Bad Request
```json
{ "detail": "Invalid date format" }
```

---

## POST /book

Create a booking for a specific date and time.

### Endpoint
```
POST /book
```

### Request Body
```json
{
  "name": "John Doe",
  "phone": "+000000000",
  "date": "2026-01-20",
  "time": "10:00:00"
}
```

### Success Response — 201 Created
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "+000000000",
  "date": "2026-01-20",
  "time": "10:00:00",
  "created_at": "2026-01-22T03:09:21.060191"
}
```

### Conflict Response — 409
```json
{ "detail": "This slot is already booked" }
```

---

## GET /ai/availability

Return available slots for a date, optionally filtered by a preference bucket.

### Endpoint
```
GET /ai/availability?date=YYYY-MM-DD&preference=any|morning|afternoon|evening
```

### Query Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| date | string | yes | Date in format `YYYY-MM-DD` |
| preference | string | no | `any` (default) or `morning|afternoon|evening` |

### Bucket Rules (MVP)
- morning: `09:00–12:00`
- afternoon: `12:00–15:00`
- evening: `15:00–17:00`

### Example
```bash
curl "http://localhost:8000/ai/availability?date=2026-01-20&preference=morning"
```

### Example Response — 200
```json
{
  "date": "2026-01-20",
  "preference": "morning",
  "available_slots": ["09:00","09:30","11:30"],
  "count": 3
}
```

### Error Responses — 400
```json
{ "detail": "Invalid date format" }
```
```json
{ "detail": "Invalid preference" }
```

---

## POST /ai/book

Smarter AI booking helper.

### Behavior
- If `time` is **missing** → returns `action="suggest"` and **ALL** available slots for the selected preference.
- If `time` is provided but **unavailable/booked** → returns `action="suggest"` and the **2 closest** available slots.
- If `time` is provided and **available** → returns `action="booked"` and creates the booking.
- If input validation fails → `400`
- If DB/API detects a conflict at final booking step → `409`

### Endpoint
```
POST /ai/book
```

### Request Body (suggest — no time)
```json
{
  "name": "Test User",
  "phone": "+000000000",
  "date": "2026-01-20",
  "preference": "morning"
}
```

### Response (suggest — no time)
```json
{
  "action": "suggest",
  "date": "2026-01-20",
  "preference": "morning",
  "requested_time": null,
  "reason": null,
  "suggestions": ["09:00","09:30","11:30"],
  "message": "Available slots:"
}
```

### Request Body (book — with time)
```json
{
  "name": "Test User",
  "phone": "+000000000",
  "date": "2026-01-20",
  "preference": "any",
  "time": "11:30"
}
```

### Response (booked)
```json
{
  "action": "booked",
  "message": "Booking confirmed.",
  "booking": {
    "id": 5,
    "name": "Test User",
    "phone": "+000000000",
    "date": "2026-01-20",
    "time": "11:30:00",
    "created_at": "2026-01-23 04:44:21.078079"
  }
}
```

### Response (requested time unavailable → suggest closest 2)
```json
{
  "action": "suggest",
  "date": "2026-01-20",
  "preference": "any",
  "requested_time": "11:30",
  "reason": "requested_time_unavailable",
  "suggestions": ["12:00","12:30"],
  "message": "11:30 is not available. Closest available slots: 12:00, 12:30"
}
```

### Error Responses

#### 400 Bad Request (invalid date or time format)
```json
{ "detail": "Invalid date format" }
```
```json
{ "detail": "Invalid time format (use HH:MM or HH:MM:SS)" }
```

#### 409 Conflict (final booking step conflict)
```json
{ "detail": "This slot is already booked" }
```
