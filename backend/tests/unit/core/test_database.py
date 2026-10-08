# backend/tests/unit/core/test_database.py
import pytest
from unittest.mock import AsyncMock, patch

from app.settings.database import DatabaseSettings
from app.core.database import DatabaseManager


@pytest.fixture
def test_settings():
    """Тестовые настройки БД, не зависящие от .env."""
    return DatabaseSettings(
        user="test_user",
        password="test_pass",
        database="test_db",
        host="localhost",
        port=5432,
        min_size=1,
        max_size=2,
        statement_timeout="5s",
        application_name="test-app",
    )


@pytest.fixture
def db_manager(test_settings):
    """Менеджер БД с тестовыми настройками для каждого теста."""
    return DatabaseManager(settings=test_settings)


class TestDatabaseManager:

    @pytest.mark.asyncio
    async def test_init_pool_is_idempotent(self, db_manager):
        mock_pool = AsyncMock()
        with patch("app.core.database.asyncpg.create_pool", new=AsyncMock(return_value=mock_pool)) as mock_create:
            await db_manager.init_pool()
            assert mock_create.call_count == 1
            
            await db_manager.init_pool()
            assert mock_create.call_count == 1
            assert db_manager._pool is mock_pool

    @pytest.mark.asyncio
    async def test_connection_raises_before_init(self):
        # Создаём менеджер БЕЗ пула, но с тестовыми настройками
        settings = DatabaseSettings(
            user="u", password="p", database="d",
            host="h", port=1, min_size=1, max_size=1,
            statement_timeout="1s", application_name="a"
        )
        db_manager = DatabaseManager(settings=settings)
        
        with pytest.raises(RuntimeError, match="Database pool not initialized"):
            async with db_manager.connection():
                pass

    @pytest.mark.asyncio
    async def test_manager_uses_settings_for_pool_creation(self, test_settings):
        db_manager = DatabaseManager(settings=test_settings)
        
        with patch("app.core.database.asyncpg.create_pool", new=AsyncMock(return_value=AsyncMock())) as mock_create:
            await db_manager.init_pool()
            
            mock_create.assert_called_once_with(
                user="test_user",
                password="test_pass",
                database="test_db",
                host="localhost",
                port=5432,
                min_size=1,
                max_size=2,
                server_settings={
                    "application_name": "test-app",
                    "statement_timeout": "5s",
                },
            )

    # ... остальные тесты аналогично используют db_manager или создают свой экземпляр ...