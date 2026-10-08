# backend/app/repositories/impl/_crud.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import asyncpg


@dataclass
class RequestRecord:
    """Полный рекорд заявки для CRUD-операций."""
    id: str
    title: str
    description: str
    status: str
    category_id: int
    assignee_id: int
    created_at: datetime


class _RequestCrudRepo:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def upsert(
        self,
        title: str,
        description: str,
        status: str,
        category_id: int,
        assignee_id: int,
        request_id: Optional[str] = None,
    ) -> RequestRecord:
        """Создать или обновить заявку через SQL-функцию upsert_request."""
        row = await self._conn.fetchrow(
            "SELECT * FROM upsert_request($1, $2, $3::request_status, $4, $5, $6)",
            title,
            description,
            status,
            category_id,
            assignee_id,
            request_id,
        )
        if not row:
            raise ValueError("upsert_request returned no rows")

        return RequestRecord(
            id=row["out_id"],
            title=row["out_title"],
            description=description,
            status=row["out_status"],
            category_id=category_id,
            assignee_id=assignee_id,
            created_at=row["out_created_at"],
        )

    async def get_by_id(self, request_id: str) -> Optional[RequestRecord]:
        """Получить заявку по UUID напрямую из таблицы requests."""
        row = await self._conn.fetchrow(
            """
            SELECT id::text, title, description, status::text, 
                   category_id, assignee_id, created_at
            FROM requests 
            WHERE id = $1
            """,
            request_id,
        )
        if not row:
            return None

        return RequestRecord(**{k: row[k] for k in RequestRecord.__dataclass_fields__})