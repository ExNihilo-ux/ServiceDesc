# backend/tests/conftest.py
import os
import pytest
import asyncpg

from app.settings.database import DatabaseSettings


@pytest.fixture
async def conn():
    """Новый пул + соединение + транзакция для КАЖДОГО интеграционного теста.
    
    Явно читает POSTGRES_* переменные окружения для создания настроек.
    Гарантирует работу независимо от расположения .env файла.
    """
    settings = DatabaseSettings(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        min_size=1,
        max_size=1,
        statement_timeout="30s",
        application_name="test-backend",
    )
    
    pool = await asyncpg.create_pool(
        user=settings.user,
        password=settings.password,
        database=settings.database,
        host=settings.host,
        port=settings.port,
        min_size=settings.min_size,
        max_size=settings.max_size,
    )
    
    async with pool.acquire() as connection:
        await connection.execute("BEGIN")
        try:
            await connection.execute("""
                INSERT INTO categories (id, name) VALUES (1, 'Test') 
                ON CONFLICT (id) DO NOTHING;
                INSERT INTO users (id, email, full_name) VALUES (1, 'test@test.com', 'Test User') 
                ON CONFLICT (id) DO NOTHING;
            """)
            yield connection
        finally:
            await connection.execute("ROLLBACK")
    
    await pool.close()