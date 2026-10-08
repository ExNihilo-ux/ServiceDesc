# backend/app/settings/app.py
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Общие настройки приложения (ML, интеграции и т.д.).
    
    Читает переменные из корневого .env файла проекта.
    Путь вычисляется динамически относительно расположения этого файла.
    """
    model_config = SettingsConfigDict(
        # Поднимаемся на 3 уровня вверх от backend/app/settings/ до корня ServiceDesc/
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "1536"))
    """Размерность вектора эмбеддинга. 
    По умолчанию 1536 для OpenAI text-embedding-3-small.
    Может быть переопределена через переменную окружения EMBEDDING_DIMENSION."""


app_settings = AppSettings()