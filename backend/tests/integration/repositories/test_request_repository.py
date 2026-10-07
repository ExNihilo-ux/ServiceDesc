# backend/tests/integration/repositories/test_request_repository.py
import pytest
from app.repositories.request_repository import RequestRepository


class TestRequestRepositoryUpsert:

    @pytest.mark.asyncio
    async def test_creates_request_with_auto_uuid(self, conn):
        repo = RequestRepository(conn)
        result = await repo.create_or_update(
            title="TDD Auto-ID", description="Test", status="new",
            category_id=1, assignee_id=1, request_id=None,
        )
        assert len(result.id) == 36
        assert result.title == "TDD Auto-ID"

    @pytest.mark.asyncio
    async def test_updates_existing_by_explicit_id(self, conn):
        repo = RequestRepository(conn)
        await repo.create_or_update(
            title="Original", description="Desc", status="new",
            category_id=1, assignee_id=1, request_id="FIXED-ID",
        )
        updated = await repo.create_or_update(
            title="Updated", description="New", status="in_progress",
            category_id=1, assignee_id=1, request_id="FIXED-ID",
        )
        assert updated.title == "Updated"