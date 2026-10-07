# backend/tests/conftest.py
import os
import pytest
import asyncpg
from dotenv import load_dotenv

load_dotenv()


def _get_db_url():
    return (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}"
        f"/{os.getenv('POSTGRES_DB')}"
    )


@pytest.fixture
async def conn():
    """Новый пул + соединение + транзакция для КАЖДОГО теста.
    
    Никаких session-scoped фикстур — нет конфликтов event loop.
    """
    pool = await asyncpg.create_pool(dsn=_get_db_url(), min_size=1, max_size=1)
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