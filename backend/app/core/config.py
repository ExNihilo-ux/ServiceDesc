# backend/app/core/config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Размерность эмбеддинга по умолчанию (OpenAI text-embedding-3-small)
    EMBEDDING_DIMENSION: int = 1536


settings = Settings()