
# Callex API

## Health
GET /health  
Response:
{ "status": "ok" }

## Get available slots
GET /slots  
Response:
[
  { "time": "2026-01-15T16:00", "available": true }
]

## Create booking
POST /book  
Body:
{
  "name": "John",
  "phone": "0501234567",
  "date": "2026-01-15",
  "time": "16:00"
}

Response:
{
  "id": 123,
  "status": "confirmed"
}
