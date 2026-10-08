# backend/app/core/database.py
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from dotenv import load_dotenv

# Загружаем переменные окружения из корневого .env файла
load_dotenv()


class DatabaseManager:
    """Асинхронный менеджер подключений к PostgreSQL через asyncpg.

    Реализует паттерн Singleton для управления жизненным циклом пула соединений.
    Гарантирует идемпотентную инициализацию и безопасное закрытие ресурсов.
    """

    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def init_pool(self) -> None:
        """Инициализация пула соединений при старте приложения.

        Метод идемпотентен: повторный вызов не создаёт новый пул и не вызывает ошибок.
        Это критически важно для E2E-тестов, где фикстура может вызывать init_pool()
        несколько раз в рамках одного процесса pytest.

        Настройки сервера:
            - application_name: идентификатор подключения для мониторинга в pg_stat_activity
            - statement_timeout: защита от зависших запросов (30 секунд)
        """
        if self._pool is not None:
            return

        self._pool = await asyncpg.create_pool(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("PORT_POSTGRES", "5432")),
            min_size=5,       # Минимальное кол-во соединений
            max_size=20,      # Максимальное кол-во соединений
            server_settings={
                "application_name": "airport-backend",
                "statement_timeout": "30s",
            },
        )

    async def close_pool(self) -> None:
        """Корректное закрытие пула при остановке приложения или завершении теста.

        Сбрасывает _pool в None, чтобы следующий вызов init_pool() создал новый пул.
        Это необходимо для изоляции E2E-тестов и корректной работы lifespan в dev-режиме.
        """
        if self._pool:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Контекстный менеджер для безопасного получения соединения из пула.

        Гарантирует возврат соединения в пул даже при возникновении исключения.
        Raises:
            RuntimeError: Если метод вызван до инициализации пула (защита от race condition).
        """
        if self._pool is None:
            raise RuntimeError("Database pool not initialized. Call init_pool() first.")

        async with self._pool.acquire() as conn:
            yield conn


db = DatabaseManager()