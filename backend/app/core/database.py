# backend/app/core/database.py
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from dotenv import load_dotenv

load_dotenv()


class DatabaseManager:
    """Асинхронный менеджер подключений к PostgreSQL через asyncpg."""

    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def init_pool(self) -> None:
        """Инициализация пула соединений при старте приложения."""
        if self._pool is not None:
            return

        self._pool = await asyncpg.create_pool(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            min_size=5,
            max_size=20,
            server_settings={
                "application_name": "airport-backend",
                "statement_timeout": "30s",
            },
        )

    async def close_pool(self) -> None:
        """Закрытие пула при остановке приложения."""
        if self._pool:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Получение соединения из пула в контекстном менеджере."""
        if self._pool is None:
            raise RuntimeError("Database pool not initialized. Call init_pool() first.")
        
        async with self._pool.acquire() as conn:
            yield conn


# Глобальный экземпляр (singleton)
db = DatabaseManager()