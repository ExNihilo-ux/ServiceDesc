# backend/app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.requests import router as requests_router
from app.core.database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения (startup/shutdown)."""
    await db.init_pool()
    yield
    await db.close_pool()


app = FastAPI(
    title="Airport Maintenance API",
    description="API для системы обслуживания аэропорта",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(requests_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}