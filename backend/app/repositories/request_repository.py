# backend/app/repositories/request_repository.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import asyncpg


@dataclass
class RequestResult:
    """Соответствует RETURNS TABLE(out_id, out_title, out_status, out_created_at)."""
    id: str
    title: str
    status: str
    created_at: datetime


class RequestRepository:
    """Репозиторий заявок через SQL-функции БД."""

    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def create_or_update(
        self,
        title: str,
        description: str,
        status: str,
        category_id: int,
        assignee_id: int,
        request_id: Optional[str] = None,
    ) -> RequestResult:
        query = """
            SELECT * FROM upsert_request(
                $1, $2, $3::request_status, $4, $5, $6
            )
        """
        row = await self._conn.fetchrow(
            query,
            title,
            description,
            status,
            category_id,
            assignee_id,
            request_id,
        )

        if row is None:
            raise ValueError("upsert_request returned no rows")

        return RequestResult(
            id=row["out_id"],
            title=row["out_title"],
            status=row["out_status"],
            created_at=row["out_created_at"],
        )