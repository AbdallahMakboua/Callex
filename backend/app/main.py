from fastapi import FastAPI
from app.api.bookings import router as bookings_router

app = FastAPI(title="Callex API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(bookings_router)
