# backend/app/schemas/base.py
from pydantic import BaseModel, field_validator


class NullableBaseModel(BaseModel):
    """Базовая модель для DTO с поддержкой явного null из JSON."""

    @classmethod
    def _nullable_field_validator(cls, field_name: str):
        """Фабрика валидаторов для nullable-полей."""
        @field_validator(field_name, mode="before")
        @classmethod
        def validate_nullable(cls, v):
            if v is None:
                return None
            return v
        return validate_nullable