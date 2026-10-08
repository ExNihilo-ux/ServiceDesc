# backend/tests/e2e/conftest.py
import pytest
from app.core.database import db


@pytest.fixture(autouse=True)
async def init_db_for_e2e():
    """Инициализирует и закрывает пул БД для каждого E2E-теста."""
    await db.init_pool()
    yield
    await db.close_pool()