# backend/app/api/v1/requests_main.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.repositories.request_repository import RequestRepository
from app.schemas.requests import CreateRequestDTO, UpdateRequestDTO, RequestResponseDTO
from .dependencies import get_db

router = APIRouter()

@router.get("/{request_id}")
async def get_request(request_id: UUID, db = Depends(get_db)):
    async with db.connection() as conn:
        repo = RequestRepository(conn)
        record = await repo.get_by_id(str(request_id))
        if not record:
            raise HTTPException(status_code=404, detail="Request not found")
        return RequestResponseDTO(**record.__dict__)

@router.post("/")  # <-- Слеш обязателен для корректной склейки с префиксом
async def create_request(dto: CreateRequestDTO, db = Depends(get_db)):
    async with db.connection() as conn:
        repo = RequestRepository(conn)
        try:
            result = await repo.create_or_update(**dto.model_dump())
            return RequestResponseDTO(**result.__dict__)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{request_id}")
async def update_request_status(request_id: UUID, dto: UpdateRequestDTO, db = Depends(get_db)):
    async with db.connection() as conn:
        repo = RequestRepository(conn)
        record = await repo.update_status(str(request_id), dto.status)
        if not record:
            raise HTTPException(status_code=404, detail="Request not found")
        return RequestResponseDTO(**record.__dict__)