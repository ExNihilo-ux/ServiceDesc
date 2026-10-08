# backend/app/schemas/types.py
from typing import Annotated, Any
from pydantic import BeforeValidator


def _validate_nullable_float_list(v: Any) -> list[float] | None:
    """
    Валидатор для nullable списка float.
    
    Позволяет явно передавать None без ошибок валидации типа.
    Если значение не None, оно проходит стандартную проверку Pydantic на list[float].
    """
    if v is None:
        return None
    return v


NullableFloatList = Annotated[
    list[float] | None,
    BeforeValidator(_validate_nullable_float_list)
]
"""
Переиспользуемый тип для полей, которые могут быть либо списком чисел, 
либо отсутствовать (None). Используется преимущественно для векторных эмбеддингов.
"""