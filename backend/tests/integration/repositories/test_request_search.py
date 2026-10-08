# backend/tests/integration/repositories/test_request_search.py
import json
import pytest
from app.repositories.request_repository import RequestRepository


def _make_embedding(value: float, dim: int = 1536) -> str:
    return json.dumps([value] * dim)


class TestFindSimilarRequests:
    """Тесты векторного поиска. Данные готовятся один раз для всех тестов класса."""

    @pytest.fixture(autouse=True)
    async def setup_search_data(self, conn):
        """Готовим поисковые данные ОДИН РАЗ перед всеми тестами класса."""
        # Очищаем только наши тестовые записи (безопасно даже если база грязная)
        await conn.execute("DELETE FROM request_ai_analyses WHERE request_id LIKE 'SEARCH-TEST-%'")
        await conn.execute("DELETE FROM requests WHERE id LIKE 'SEARCH-TEST-%'")

        # Создаём эталонные данные
        for i, (req_id, title, val) in enumerate([
            ("SEARCH-TEST-HIGH", "High Similarity", 0.9),
            ("SEARCH-TEST-LOW", "Low Similarity", 0.1),
            ("SEARCH-TEST-EXACT", "Exact Match", 0.5),
        ]):
            await conn.execute("""
                INSERT INTO requests (id, title, description, status, category_id, assignee_id)
                VALUES ($1, $2, 'Test', 'new'::request_status, 1, 1)
                ON CONFLICT (id) DO NOTHING
            """, req_id, title)
            
            await conn.execute(
                "INSERT INTO request_ai_analyses (request_id, summary, embedding) VALUES ($1, $2, $3::vector)",
                req_id, title, _make_embedding(val)
            )

    @pytest.mark.asyncio
    async def test_returns_empty_for_null_embedding(self, conn):
        repo = RequestRepository(conn)
        results = await repo.find_similar(embedding=None, threshold=0.7, limit=5)
        assert results == []

    @pytest.mark.asyncio
    async def test_returns_exact_match(self, conn):
        """Поиск по тому же вектору возвращает similarity=1.0."""
        repo = RequestRepository(conn)
        
        results = await repo.find_similar(
            embedding=[0.5] * 1536, threshold=1.0, limit=5
        )
        
        exact_matches = [r for r in results if r["request_id"] == "SEARCH-TEST-EXACT"]
        assert len(exact_matches) == 1
        assert abs(exact_matches[0]["similarity"] - 1.0) < 0.001

    @pytest.mark.asyncio
    async def test_filters_by_threshold(self, conn):
        """Порог отсекает нерелевантные результаты."""
        repo = RequestRepository(conn)
        
        # Ищем по вектору 0.9 с высоким порогом
        results = await repo.find_similar(
            embedding=[0.9] * 1536, threshold=0.95, limit=10
        )
        
        ids = [r["request_id"] for r in results]
        assert "SEARCH-TEST-HIGH" in ids  # Близкий вектор проходит
        assert "SEARCH-TEST-LOW" not in ids  # Далёкий вектор отфильтрован

    @pytest.mark.asyncio
    async def test_respects_limit(self, conn):
        """Limit ограничивает количество результатов."""
        repo = RequestRepository(conn)
        
        results = await repo.find_similar(
            embedding=[0.5] * 1536, threshold=0.5, limit=2
        )
        
        assert len(results) <= 2