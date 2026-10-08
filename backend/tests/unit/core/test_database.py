# backend/tests/unit/core/test_database.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.core.database import DatabaseManager


class TestDatabaseManager:
    """Unit-тесты контракта DatabaseManager."""

    @pytest.fixture
    def db_manager(self):
        """Свежий экземпляр для каждого теста (изоляция)."""
        return DatabaseManager()

    @pytest.mark.asyncio
    async def test_init_pool_is_idempotent(self):
        """Повторный вызов init_pool не должен создавать новый пул."""
        db_manager = DatabaseManager()
        
        mock_pool = AsyncMock()
        
        with patch("app.core.database.asyncpg.create_pool", new=AsyncMock(return_value=mock_pool)) as mock_create:
            
            await db_manager.init_pool()
            assert mock_create.call_count == 1
            
            await db_manager.init_pool()
            assert mock_create.call_count == 1
            
            assert db_manager._pool is mock_pool    

    @pytest.mark.asyncio
    async def test_connection_yields_and_returns_conn(self, db_manager):
        """Контекстный менеджер должен выдавать соединение и возвращать его в пул."""
        mock_conn = AsyncMock()
        mock_acquire_ctx = MagicMock()
        mock_acquire_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_acquire_ctx.__aexit__ = AsyncMock(return_value=None)
            
        mock_pool = MagicMock()
        mock_pool.acquire.return_value = mock_acquire_ctx
        db_manager._pool = mock_pool
            
        async with db_manager.connection() as conn:
            assert conn is mock_conn
            
        # Проверяем, что соединение было получено И возвращено
        mock_pool.acquire.assert_called_once()
        mock_acquire_ctx.__aenter__.assert_called_once()
        mock_acquire_ctx.__aexit__.assert_called_once()

    @pytest.mark.asyncio
    async def test_connection_raises_if_not_initialized(self, db_manager):
        """Попытка получить соединение до инициализации должна выбросить RuntimeError."""
        with pytest.raises(RuntimeError, match="Database pool not initialized"):
            async with db_manager.connection():
                pass

    @pytest.mark.asyncio
    async def test_close_pool_resets_state(self, db_manager):
        """Закрытие пула должно сбрасывать внутреннее состояние в None."""
        mock_pool = AsyncMock()
        db_manager._pool = mock_pool
         
        await db_manager.close_pool()
         
        mock_pool.close.assert_called_once()
        assert db_manager._pool is None

    @pytest.mark.asyncio
    async def test_connection_raises_before_init(self):
        """Попытка получить соединение до init_pool должна вызвать RuntimeError."""
        db_manager = DatabaseManager()
        with pytest.raises(RuntimeError, match="Database pool not initialized"):
            async with db_manager.connection():
                pass

# backend/tests/unit/core/test_database.py (дополни)
from app.core.settings import DatabaseSettings

@pytest.mark.asyncio
async def test_manager_uses_settings_for_pool_creation(self):
    """DatabaseManager должен создавать пул с параметрами из DatabaseSettings."""
    settings = DatabaseSettings(
        user="test_user",
        password="test_pass",
        database="test_db",
        host="test_host",
        port=9999,
        min_size=1,
        max_size=2,
        statement_timeout="5s",
        application_name="test-app",
    )
    
    db_manager = DatabaseManager(settings=settings)
    
    with patch("app.core.database.asyncpg.create_pool", new=AsyncMock(return_value=AsyncMock())) as mock_create:
        await db_manager.init_pool()
        
        # Проверяем, что create_pool вызван с правильными параметрами
        mock_create.assert_called_once_with(
            user="test_user",
            password="test_pass",
            database="test_db",
            host="test_host",
            port=9999,
            min_size=1,
            max_size=2,
            server_settings={
                "application_name": "test-app",
                "statement_timeout": "5s",
            },
        )