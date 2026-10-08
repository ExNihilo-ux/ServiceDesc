# backend/tests/e2e/requests/test_requests_search.py
import json
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


def _make_embedding(value: float, dim: int = 1536) -> list[float]:
    """Создаёт вектор для передачи в JSON."""
    return [value] * dim


class TestSearchRequestsEndpoint:

    @pytest.mark.asyncio
    async def test_search_returns_similar_requests(self):
        """Поиск по эмбеддингу возвращает релевантные заявки."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/requests/search",
                json={
                    "embedding": _make_embedding(0.5),
                    "threshold": 0.7,
                    "limit": 5,
                },
            )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_search_with_null_embedding_returns_empty(self):
        """NULL-эмбеддинг должен вернуть пустой список, а не ошибку."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/requests/search",
                json={
                    "embedding": None,
                    "threshold": 0.7,
                    "limit": 5,
                },
            )

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_search_invalid_threshold_returns_422(self):
        """Невалидный порог (< 0 или > 1) возвращает 422."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/requests/search",
                json={
                    "embedding": _make_embedding(0.5),
                    "threshold": -1.0,  # Невалидное значение
                    "limit": 5,
                },
            )

        assert response.status_code == 422