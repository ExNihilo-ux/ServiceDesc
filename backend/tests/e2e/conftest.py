# backend/tests/e2e/conftest.py
import os
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.database import get_db_manager
from app.settings.database import DatabaseSettings
from app.api.v1.dependencies import get_db


@pytest.fixture(autouse=True)
async def init_db_for_e2e():
    """Инициализирует БД и переопределяет зависимость для всех E2E-тестов."""
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
    
    db = get_db_manager(settings=settings)
    await db.init_pool()
    
    # Переопределяем зависимость get_db на наш предсозданный менеджер
    app.dependency_overrides[get_db] = lambda: db
    
    yield
    
    # Очищаем override после теста
    app.dependency_overrides.clear()
    await db.close_pool()


@pytest.fixture
async def client():
    """Фикстура HTTP-клиента, который автоматически следует за редиректами."""
    transport = ASGITransport(app=app)
    # follow_redirects=True решает проблему 307 кода при обращении к /requests вместо /requests/
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as c:
        yield c