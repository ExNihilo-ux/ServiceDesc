# backend/app/api/requests.py
from fastapi import APIRouter, HTTPException

from app.core.database import db
from app.repositories.request_repository import RequestRepository
from app.schemas.request_schemas import CreateRequestDTO

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("")
async def create_request(dto: CreateRequestDTO):
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
            return {
                "out_id": result.id,
                "out_title": result.title,
                "out_status": result.status,
                "out_created_at": result.created_at.isoformat(),
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))