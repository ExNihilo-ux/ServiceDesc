# backend/tests/e2e/requests/test_requests_get.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestGetRequestEndpoint:

    @pytest.mark.asyncio
    async def test_returns_request_by_id(self):
        """Успешное получение существующей заявки."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # Сначала создаём заявку
            create_resp = await client.post(
                "/requests",
                json={
                    "title": "Test Get Request",
                    "description": "Testing GET endpoint",
                    "status": "new",
                    "category_id": 1,
                    "assignee_id": 1,
                },
            )
            request_id = create_resp.json()["id"]

            # Получаем её по ID
            response = await client.get(f"/requests/{request_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == request_id
        assert data["title"] == "Test Get Request"
        assert data["status"] == "new"

    @pytest.mark.asyncio
    async def test_returns_404_for_nonexistent_id(self):
        """Несуществующий ID возвращает 404."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/requests/00000000-0000-0000-0000-000000000000")

        assert response.status_code == 404