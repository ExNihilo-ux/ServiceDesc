# backend/app/settings/database.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        env_prefix="POSTGRES_",
        extra="ignore"
    )

    user: str
    password: str
    database: str
    host: str
    port: int
    min_size: int
    max_size: int
    statement_timeout: str
    application_name: str