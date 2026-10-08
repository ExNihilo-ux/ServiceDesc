# backend/app/schemas/requests/update.py
from pydantic import BaseModel, Field


class UpdateRequestDTO(BaseModel):
    """DTO для частичного обновления заявки."""
    
    status: str = Field(
        ...,
        pattern="^(new|in_progress|resolved|cancelled)$",
        description="Новый статус заявки",
    )