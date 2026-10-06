# backend/app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="Airport Maintenance API",
    description="API для системы обслуживания аэропорта",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}