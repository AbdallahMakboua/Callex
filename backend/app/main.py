from fastapi import FastAPI

app = FastAPI(title="Callex API")

@app.get("/health")
def health():
    return {"status": "ok"}
