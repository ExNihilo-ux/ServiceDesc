# backend/app/settings/database.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Настройки подключения к PostgreSQL и управления пулом соединений.
    
    Автоматически читает переменные окружения с префиксом POSTGRES_ 
    из корневого .env файла проекта.
    """
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="POSTGRES_",
        extra="ignore"
    )

    user: str
    """Имя пользователя базы данных (POSTGRES_USER)."""

    password: str
    """Пароль пользователя базы данных (POSTGRES_PASSWORD)."""

    database: str
    """Название базы данных (POSTGRES_DB)."""

    host: str
    """Хост сервера БД. Для локальной разработки обычно localhost (POSTGRES_HOST)."""

    port: int
    """Порт подключения к PostgreSQL (POSTGRES_PORT)."""

    min_size: int
    """Минимальное количество всегда открытых соединений в пуле (POSTGRES_MIN_SIZE)."""

    max_size: int
    """Максимальное количество одновременных соединений в пуле (POSTGRES_MAX_SIZE)."""

    statement_timeout: str
    """Таймаут выполнения SQL-запросов. Защита от зависших транзакций (POSTGRES_STATEMENT_TIMEOUT)."""

    application_name: str
    """Имя приложения для мониторинга в pg_stat_activity (POSTGRES_APPLICATION_NAME)."""