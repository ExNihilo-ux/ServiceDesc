# backend/tests/e2e/requests/test_requests_delete.py
import pytest


class TestDeleteRequestEndpoint:

    @pytest.mark.asyncio
    async def test_deletes_request_successfully(self, client):
        """Успешное удаление существующей заявки."""
        create_resp = await client.post(
            "/requests",
            json={
                "title": "Test Delete Request",
                "description": "Checking DELETE endpoint",
                "status": "new",
                "category_id": 1,
                "assignee_id": 1,
            },
        )
        request_id = create_resp.json()["id"]

        delete_resp = await client.delete(f"/requests/{request_id}")
        assert delete_resp.status_code == 204

        get_resp = await client.get(f"/requests/{request_id}")
        assert get_resp.status_code == 404

    @pytest.mark.asyncio
    async def test_returns_404_for_nonexistent_id(self, client):
        """Удаление несуществующей заявки возвращает 404."""
        response = await client.delete("/requests/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404