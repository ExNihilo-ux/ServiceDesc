import os
import sys
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Добавляем корень проекта в путь для корректного импорта app.*
sys.path.append(str(Path(__file__).resolve().parent.parent))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импортируем метаданные и модели. 
# В SQL-first подходе target_metadata нужен только для проверки целостности графа миграций,
# а не для автогенерации DDL.
from app.core.database import Base
from app.models import request, user 

target_metadata = Base.metadata 

def get_sync_url():
    """Формирует синхронный URL подключения через psycopg2.
    
    Alembic требует синхронный драйвер, даже если приложение использует asyncpg.
    Переменные окружения читаются напрямую, так как .env загружается до запуска Alembic.
    """
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

def run_migrations_offline() -> None:
    """Выполняет миграции в офлайн-режиме (генерация SQL без подключения к БД).
    
    Используется для генерации скриптов деплоя или аудита изменений.
    literal_binds=True подставляет значения параметров прямо в SQL-текст.
    """
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Выполняет миграции в онлайн-режиме (прямое подключение к БД).
    
    Основной режим работы при разработке и деплое.
    NullPool используется, чтобы избежать проблем с пулом соединений в CLI-инструменте.
    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_sync_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

# Точка входа: определяем режим работы по флагу --sql (офлайн) или подключению (онлайн)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()