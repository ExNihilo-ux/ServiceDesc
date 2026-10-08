# backend/app/schemas/types.py
from typing import Annotated, Any
from pydantic import BeforeValidator


def _validate_nullable_float_list(v: Any) -> list[float] | None:
    """Валидатор для nullable списка float. Пропускает None как есть."""
    if v is None:
        return None
    return v


NullableFloatList = Annotated[
    list[float] | None,
    BeforeValidator(_validate_nullable_float_list)
]