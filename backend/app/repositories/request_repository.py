# backend/app/repositories/request_repository.py
from typing import Optional
import asyncpg

from .impl._crud import _RequestCrudRepo, RequestRecord
from .impl._search import _RequestSearchRepo, SimilarRequest


class RequestRepository:
    """Единая точка входа для работы с заявками.
    
    Делегирует операции специализированным внутренним репозиториям.
    Роутеры и сервисы работают ТОЛЬКО с этим классом.
    """

    def __init__(self, conn: asyncpg.Connection):
        self._crud = _RequestCrudRepo(conn)
        self._search = _RequestSearchRepo(conn)

    async def create_or_update(self, **kwargs) -> RequestRecord:
        return await self._crud.upsert(**kwargs)

    async def get_by_id(self, request_id: str) -> Optional[RequestRecord]:
        return await self._crud.get_by_id(request_id)

    async def find_similar(self, **kwargs) -> list[SimilarRequest]:
        return await self._search.find_similar(**kwargs)