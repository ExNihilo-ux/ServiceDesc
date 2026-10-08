# backend/app/core/database.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg

from app.settings.database import DatabaseSettings


class DatabaseManager:
    """Асинхронный менеджер подключений к PostgreSQL через asyncpg."""

    def __init__(self, settings: DatabaseSettings | None = None):
        self._settings = settings or DatabaseSettings()
        self._pool: asyncpg.Pool | None = None

    async def init_pool(self) -> None:
        if self._pool is not None:
            return

        self._pool = await asyncpg.create_pool(
            user=self._settings.user,
            password=self._settings.password,
            database=self._settings.database,
            host=self._settings.host,
            port=self._settings.port,
            min_size=self._settings.min_size,
            max_size=self._settings.max_size,
            server_settings={
                "application_name": self._settings.application_name,
                "statement_timeout": self._settings.statement_timeout,
            },
        )

    async def close_pool(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        if self._pool is None:
            raise RuntimeError("Database pool not initialized. Call init_pool() first.")
        async with self._pool.acquire() as conn:
            yield conn


def get_db_manager(settings: DatabaseSettings | None = None) -> DatabaseManager:
    """Фабрика для получения менеджера БД.
    
    В тестах и E2E всегда передавай settings явно.
    В dev-режиме можно вызвать без аргументов (прочитает .env).
    """
    return DatabaseManager(settings)
