from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Общие настройки приложения (ML, интеграции и т.д.)."""
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    EMBEDDING_DIMENSION: int = 1536


app_settings = AppSettings()