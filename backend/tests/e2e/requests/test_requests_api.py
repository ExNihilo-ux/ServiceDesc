# backend/tests/e2e/requests/test_requests_api.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestCreateRequestEndpoint:
    """E2E тесты для POST /requests"""

    @pytest.mark.asyncio
    async def test_create_request_success(self):
        """Успешное создание заявки возвращает 200 и UUID."""
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
        assert "out_id" in data
        assert len(data["out_id"]) == 36
        assert data["out_title"] == "E2E Test Request"

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