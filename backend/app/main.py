# backend/app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.requests import router as requests_router
from app.core.database import get_db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения (startup/shutdown).
    
    Инициализирует пул соединений к БД перед запуском сервера 
    и корректно закрывает его при остановке приложения.
    """
    # Создаём менеджер БД с настройками из .env
    db = get_db_manager()
    
    # Поднимаем пул соединений (идемпотентно)
    await db.init_pool()
    
    yield  # Приложение работает и обрабатывает запросы
    
    # Корректно закрываем все соединения при выключении
    await db.close_pool()


app = FastAPI(
    title="Airport Maintenance API",
    description="API для системы автоматизированной обработки заявок на обслуживание аэропорта",
    version="0.1.0",
    lifespan=lifespan,
)

# Подключаем роутеры заявок
app.include_router(requests_router)


@app.get("/health")
async def health_check():
    """Эндпоинт проверки работоспособности сервиса (для балансировщиков и мониторинга)."""
    return {"status": "ok"}