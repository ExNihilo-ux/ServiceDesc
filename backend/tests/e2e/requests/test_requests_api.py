# backend/tests/e2e/requests/test_requests_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestCreateRequestEndpoint:
    """E2E тесты для POST /requests"""

    @pytest.mark.asyncio
    async def test_create_request_success(self):
        """Успешное создание заявки возвращает 200 и корректный DTO."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/requests",
                json={
                    "title": "E2E Test Request",
                    "description": "Testing full HTTP cycle",
                    "status": "new",
                    "category_id": 1,
                    "assignee_id": 1,
                },
            )

        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert len(data["id"]) == 36 
        assert data["title"] == "E2E Test Request"
        assert data["description"] == "Testing full HTTP cycle"
        assert data["status"] == "new"
        assert data["category_id"] == 1
        assert data["assignee_id"] == 1
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_request_invalid_status(self):
        """Невалидный статус возвращает 422."""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/requests",
                json={
                    "title": "Bad Status",
                    "description": "Should fail validation",
                    "status": "INVALID_STATUS",
                    "category_id": 1,
                    "assignee_id": 1,
                },
            )

        assert response.status_code == 422