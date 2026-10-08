# backend/app/repositories/impl/_search.py
import json
from dataclasses import dataclass
import asyncpg


@dataclass
class SimilarRequest:
    request_id: str
    title: str
    similarity: float


class _RequestSearchRepo:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def find_similar(self, embedding: list[float] | None, threshold=0.7, limit=5) -> list[SimilarRequest]:
        if not embedding:
            return []
        rows = await self._conn.fetch(
            "SELECT request_id, title, similarity FROM find_similar_requests($1::vector, $2, $3)",
            json.dumps(embedding), threshold, limit
        )
        return [SimilarRequest(r["request_id"], r["title"], float(r["similarity"])) for r in rows]