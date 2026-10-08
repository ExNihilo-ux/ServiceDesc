# backend/app/api/v1/requests_search.py
from fastapi import APIRouter, Depends

from app.repositories.request_repository import RequestRepository
from app.schemas.requests import SearchRequestDTO
from .dependencies import get_db

router = APIRouter()

@router.post("/search")
async def search_requests(dto: SearchRequestDTO, db = Depends(get_db)):
    async with db.connection() as conn:
        repo = RequestRepository(conn)
        return await repo.find_similar(
            embedding=dto.embedding,
            threshold=dto.threshold,
            limit=dto.limit,
        )