# backend/tests/e2e/requests/test_requests_get.py
import pytest


class TestGetRequestEndpoint:

    @pytest.mark.asyncio
    async def test_returns_request_by_id(self, client):
        """Успешное получение существующей заявки."""
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

        response = await client.get(f"/requests/{request_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == request_id
        assert data["title"] == "Test Get Request"
        assert data["status"] == "new"

    @pytest.mark.asyncio
    async def test_returns_404_for_nonexistent_id(self, client):
        """Несуществующий ID возвращает 404."""
        response = await client.get("/requests/00000000-0000-0000-0000-000000000000")

        assert response.status_code == 404