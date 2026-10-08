# backend/app/api/v1/requests.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.core.database import DatabaseManager, get_db_manager
from app.repositories.request_repository import RequestRepository
from app.schemas.requests import CreateRequestDTO, SearchRequestDTO, RequestResponseDTO

router = APIRouter(prefix="/requests", tags=["Requests"])


def get_db() -> DatabaseManager:
    """Зависимость для получения менеджера БД."""
    return get_db_manager()


@router.get("/{request_id}")
async def get_request(
    request_id: UUID,
    db: DatabaseManager = Depends(get_db),
):
    """Получить заявку по ID."""
    async with db.connection() as conn:
        repo = RequestRepository(conn)
        record = await repo.get_by_id(str(request_id))

        if not record:
            raise HTTPException(status_code=404, detail="Request not found")

        return RequestResponseDTO(
            id=record.id,
            title=record.title,
            description=record.description,
            status=record.status,
            category_id=record.category_id,
            assignee_id=record.assignee_id,
            created_at=record.created_at,
        )


@router.post("")
async def create_request(
    dto: CreateRequestDTO,
    db: DatabaseManager = Depends(get_db),
):
    async with db.connection() as conn:
        repo = RequestRepository(conn)
        try:
            result = await repo.create_or_update(
                title=dto.title,
                description=dto.description,
                status=dto.status,
                category_id=dto.category_id,
                assignee_id=dto.assignee_id,
            )
            # Единый формат ответа через DTO (убраны префиксы out_)
            return RequestResponseDTO(
                id=result.id,
                title=result.title,
                description=result.description,
                status=result.status,
                category_id=result.category_id,
                assignee_id=result.assignee_id,
                created_at=result.created_at,
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.post("/search")
async def search_requests(
    dto: SearchRequestDTO,
    db: DatabaseManager = Depends(get_db),
):
    async with db.connection() as conn:
        repo = RequestRepository(conn)
        results = await repo.find_similar(
            embedding=dto.embedding,
            threshold=dto.threshold,
            limit=dto.limit,
        )
        return results