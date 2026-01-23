Perfect.
Below is **pure Copy → Paste content**, **each file isolated**, **defaults applied**
(09:00–17:00, 60-minute slots).
No explanations. No mixing.

---

## `docs/API.md`

# Callex API Documentation

Base URL (local):
```

[http://localhost:8000](http://localhost:8000)

```

---

## GET /slots

Return available booking slots for a given date.

### Endpoint
```

GET /slots

````

### Query Parameters

| Name | Type | Required | Description |
|----|----|----|----|
| date | string | yes | Date in format `YYYY-MM-DD` |

### Business Rules
- Working hours: **09:00 → 17:00**
- Slot duration: **60 minutes**
- Slots already booked are marked unavailable

---

### Example Request

```bash
curl "http://localhost:8000/slots?date=2026-01-20"
````

---

### Example Response

```json
{
  "date": "2026-01-20",
  "timezone": "local",
  "slots": [
    { "time": "09:00:00", "available": true },
    { "time": "10:00:00", "available": false },
    { "time": "11:00:00", "available": true },
    { "time": "12:00:00", "available": true },
    { "time": "13:00:00", "available": true },
    { "time": "14:00:00", "available": true },
    { "time": "15:00:00", "available": true },
    { "time": "16:00:00", "available": true }
  ]
}
```

---

### Error Responses

#### 400 Bad Request

```json
{
  "detail": "Invalid or missing date parameter"
}
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

---

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

---

### Conflict Response — 409

```json
{
  "detail": "This slot is already booked"
}
```

````
## GET /ai/availability

Return available slots for a date, optionally filtered by a preference bucket.

### Endpoint

### Example
```bash
curl "http://localhost:8000/ai/availability?date=2026-01-20&preference=morning"
```