# backend/app/repositories/request_repository.py
from typing import Optional
import asyncpg

from .impl._crud import _RequestCrudRepo, RequestRecord
from .impl._search import _RequestSearchRepo, SimilarRequest


class RequestRepository:
    """Единая точка входа (Facade) для работы с заявками.
    
    Инкапсулирует сложную внутреннюю структуру репозиториев.
    Роутеры и сервисы работают ТОЛЬКО с этим классом, не импортируя impl/.
    """

    def __init__(self, conn: asyncpg.Connection):
        # Инициализируем специализированные репозитории через композицию
        self._crud = _RequestCrudRepo(conn)
        self._search = _RequestSearchRepo(conn)

    async def create_or_update(self, **kwargs) -> RequestRecord:
        """Создать новую заявку или обновить существующую (upsert)."""
        return await self._crud.upsert(**kwargs)

    async def get_by_id(self, request_id: str) -> Optional[RequestRecord]:
        """Получить полную информацию о заявке по её UUID."""
        return await self._crud.get_by_id(request_id)

    async def update_status(self, request_id: str, new_status: str) -> Optional[RequestRecord]:
        """
        Обновить статус заявки.
        
        Args:
            request_id: UUID заявки.
            new_status: Новый статус (new, in_progress, resolved, cancelled).
            
        Returns:
            Обновленную запись или None, если заявка не найдена.
        """
        return await self._crud.update_status(request_id, new_status)

    async def find_similar(self, **kwargs) -> list[SimilarRequest]:
        """Найти похожие заявки с помощью векторного поиска (pgvector)."""
        return await self._search.find_similar(**kwargs)

    async def delete_by_id(self, request_id: str) -> bool:
        """Удалить заявку и связанные с ней данные (каскадно)."""
        return await self._crud.delete_by_id(request_id)