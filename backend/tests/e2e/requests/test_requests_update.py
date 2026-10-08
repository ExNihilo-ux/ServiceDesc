# backend/tests/e2e/requests/test_requests_update.py
import pytest


class TestUpdateRequestEndpoint:

    @pytest.mark.asyncio
    async def test_updates_request_status(self, client):
        """Успешное обновление статуса существующей заявки."""
        # 1. Создаём заявку
        create_resp = await client.post(
            "/requests",
            json={
                "title": "Test Update Status",
                "description": "Checking PATCH endpoint",
                "status": "new",
                "category_id": 1,
                "assignee_id": 1,
            },
        )
        request_id = create_resp.json()["id"]

        # 2. Обновляем статус
        update_resp = await client.patch(
            f"/requests/{request_id}",
            json={"status": "in_progress"},
        )

        assert update_resp.status_code == 200
        data = update_resp.json()
        assert data["status"] == "in_progress"
        assert data["id"] == request_id

    @pytest.mark.asyncio
    async def test_returns_404_for_nonexistent_id(self, client):
        """Обновление несуществующей заявки возвращает 404."""
        response = await client.patch(
            "/requests/00000000-0000-0000-0000-000000000000",
            json={"status": "resolved"},
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_rejects_invalid_status(self, client):
        """Передача невалидного статуса возвращает 422."""
        # Сначала создаём, чтобы был валидный ID
        create_resp = await client.post(
            "/requests",
            json={
                "title": "Test Invalid Status",
                "description": "Should fail validation",
                "status": "new",
                "category_id": 1,
                "assignee_id": 1,
            },
        )
        request_id = create_resp.json()["id"]

        response = await client.patch(
            f"/requests/{request_id}",
            json={"status": "INVALID_STATUS"},
        )

        assert response.status_code == 422