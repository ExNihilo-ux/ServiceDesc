# backend/app/schemas/requests/response.py (обновлённая версия)
from datetime import datetime
from pydantic import BaseModel


class RequestResponseDTO(BaseModel):
    """DTO для ответа при получении заявки."""
    id: str
    title: str
    description: str
    status: str
    category_id: int
    assignee_id: int
    created_at: datetime