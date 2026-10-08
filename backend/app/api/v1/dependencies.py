# backend/app/api/v1/dependencies.py
from app.core.database import DatabaseManager, get_db_manager


def get_db() -> DatabaseManager:
    """Зависимость для получения менеджера БД."""
    return get_db_manager()