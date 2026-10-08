# backend/tests/unit/schemas/test_embedding_validator.py
import pytest
from unittest.mock import patch

from app.schemas.validators import EmbeddingValidator


class TestEmbeddingValidator:
    """Unit-тесты для валидации векторных эмбеддингов заявок."""

    def test_allows_none(self):
        """Явный null должен приниматься без ошибок."""
        result = EmbeddingValidator.validate(None)
        assert result is None

    def test_allows_valid_float_list(self):
        """Валидный список float проходит проверку."""
        data = [0.1, 0.5, -0.3, 0.9]
        with patch("app.schemas.validators.app_settings") as mock_settings:
            mock_settings.EMBEDDING_DIMENSION = 4
            result = EmbeddingValidator.validate(data)
        assert result == data

    def test_rejects_string(self):
        """Строка должна вызывать ValueError."""
        with pytest.raises(ValueError, match="must be a list"):
            EmbeddingValidator.validate("not a list")

    def test_converts_int_to_float(self):
        """Список целых чисел должен приводиться к float."""
        data = [1, 2, 3]
        with patch("app.schemas.validators.app_settings") as mock_settings:
            mock_settings.EMBEDDING_DIMENSION = 3
            result = EmbeddingValidator.validate(data)
        assert all(isinstance(v, float) for v in result)
        assert result == [1.0, 2.0, 3.0]

    def test_rejects_nested_list(self):
        """Вложенные списки недопустимы."""
        with pytest.raises(ValueError, match="must be numeric"):
            EmbeddingValidator.validate([[0.1], [0.2]])

    def test_rejects_empty_list(self):
        """Пустой вектор бессмысленен для поиска прецедентов."""
        with pytest.raises(ValueError, match="cannot be empty"):
            EmbeddingValidator.validate([])

    def test_rejects_wrong_dimension(self):
        """Вектор неверной размерности должен отклоняться."""
        with patch("app.schemas.validators.app_settings") as mock_settings:
            mock_settings.EMBEDDING_DIMENSION = 1536
            wrong_dim = [0.5] * 100
            with pytest.raises(ValueError, match="dimension must be 1536"):
                EmbeddingValidator.validate(wrong_dim)

    def test_accepts_configured_dimension(self):
        """Ровно настроенная размерность — валидно."""
        with patch("app.schemas.validators.app_settings") as mock_settings:
            mock_settings.EMBEDDING_DIMENSION = 1536
            correct = [0.5] * 1536
            result = EmbeddingValidator.validate(correct)
        assert len(result) == 1536