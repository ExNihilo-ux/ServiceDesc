# backend/app/schemas/validators.py
from typing import Any

from app.core.config import settings


class EmbeddingValidator:
    """Валидатор векторных эмбеддингов для поиска исторических прецедентов.

    Проверяет тип данных, непустоту и соответствие размерности модели ИИ,
    заданной через EMBEDDING_DIMENSION в .env.
    """

    @classmethod
    def validate(cls, value: Any) -> list[float] | None:
        if value is None:
            return None

        if not isinstance(value, list):
            raise ValueError("embedding must be a list of floats or null")

        if len(value) == 0:
            raise ValueError("embedding cannot be empty")

        try:
            float_list = [float(v) for v in value]
        except (TypeError, ValueError) as e:
            raise ValueError(f"all embedding values must be numeric: {e}")

        expected_dim = settings.EMBEDDING_DIMENSION
        if len(float_list) != expected_dim:
            raise ValueError(
                f"embedding dimension must be {expected_dim}, "
                f"got {len(float_list)}"
            )

        return float_list