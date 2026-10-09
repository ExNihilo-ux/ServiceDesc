# backend/tests/unit/services/test_ai_service.py
import pytest
from app.services.ai_service import AIService


class TestAIService:
    """Unit-тесты для ИИ-сервиса с реальной ML-моделью."""

    @pytest.fixture(scope="class")
    def ai_service(self):
        # Модель тяжелая, загружаем один раз на класс
        return AIService()

    def test_classifies_roof_issue(self, ai_service):
        """Эвристика определяет категорию 'Кровля'."""
        category_id = ai_service.classify_text("В терминале B течет крыша над выходом 5")
        assert category_id == 1

    def test_semantic_similarity_works(self, ai_service):
        """Модель понимает смысл: 'свет' ближе к 'лампе', чем к 'воде'."""
        emb_light_1 = ai_service.generate_embedding("Не работает освещение в цеху")
        emb_light_2 = ai_service.generate_embedding("Сгорели лампы на складе")
        emb_water = ai_service.generate_embedding("Прорвало трубу с водой")

        dist_similar = self._cosine_distance(emb_light_1, emb_light_2)
        dist_different = self._cosine_distance(emb_light_1, emb_water)

        assert dist_similar < dist_different

    def test_generates_correct_dimension(self, ai_service):
        """Вектор должен иметь размерность 1024 (как у модели E5 Large)."""
        embedding = ai_service.generate_embedding("Test description")
        assert len(embedding) == 1024
        assert all(isinstance(x, float) for x in embedding)

    def _cosine_distance(self, v1, v2):
        import math
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        return 1 - (dot_product / (norm1 * norm2))