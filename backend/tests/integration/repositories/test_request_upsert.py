# backend/tests/integration/repositories/test_request_upsert.py
import pytest
import asyncpg
from app.repositories.request_repository import RequestRepository


class TestRequestUpsert:
    """Тесты создания и обновления заявок."""

    @pytest.mark.asyncio
    async def test_creates_request_with_auto_uuid(self, conn):
        repo = RequestRepository(conn)
        result = await repo.create_or_update(
            title="Auto-ID Test", description="Test", status="new",
            category_id=1, assignee_id=1, request_id=None,
        )
        assert len(result.id) == 36
        assert result.title == "Auto-ID Test"

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

    @pytest.mark.asyncio
    async def test_fails_on_invalid_category_id(self, conn):
        repo = RequestRepository(conn)
        with pytest.raises(asyncpg.exceptions.ForeignKeyViolationError):
            await repo.create_or_update(
                title="Bad Category", description="Fail", status="new",
                category_id=9999, assignee_id=1, request_id=None,
            )

    @pytest.mark.asyncio
    async def test_fails_on_invalid_assignee_id(self, conn):
        repo = RequestRepository(conn)
        with pytest.raises(asyncpg.exceptions.ForeignKeyViolationError):
            await repo.create_or_update(
                title="Bad Assignee", description="Fail", status="new",
                category_id=1, assignee_id=9999, request_id=None,
            )