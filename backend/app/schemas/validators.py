# backend/app/schemas/validators.py
from typing import Any

from app.settings.app import app_settings


class EmbeddingValidator:
    """Валидатор векторных эмбеддингов для поиска исторических прецедентов.

    Проверяет тип данных, непустоту и соответствие размерности модели ИИ,
    заданной через EMBEDDING_DIMENSION в .env.
    """

    @classmethod
    def validate(cls, value: Any) -> list[float] | None:
        """
        Валидирует входное значение как список float заданной размерности.
        
        Args:
            value: Входные данные (могут быть None, списком int/float или ошибочным типом).
            
        Returns:
            Список float той же длины, что и EMBEDDING_DIMENSION, или None.
            
        Raises:
            ValueError: Если тип неверен, список пуст или размерность не совпадает.
        """
        # 1. Разрешаем явный null (например, если эмбеддинг ещё не сгенерирован)
        if value is None:
            return None

        # 2. Проверка типа: ожидаем только список
        if not isinstance(value, list):
            raise ValueError("embedding must be a list of floats or null")

        # 3. Защита от пустых векторов (бессмысленны для поиска)
        if len(value) == 0:
            raise ValueError("embedding cannot be empty")

        # 4. Безопасное приведение типов (int -> float) с проверкой на мусор
        try:
            float_list = [float(v) for v in value]
        except (TypeError, ValueError) as e:
            raise ValueError(f"all embedding values must be numeric: {e}")

        # 5. Строгая проверка размерности согласно конфигурации модели ИИ
        expected_dim = app_settings.EMBEDDING_DIMENSION
        if len(float_list) != expected_dim:
            raise ValueError(
                f"embedding dimension must be {expected_dim}, "
                f"got {len(float_list)}"
            )

        return float_list