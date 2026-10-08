# backend/app/schemas/request_schemas.py
from pydantic import BaseModel, Field

from app.schemas.types import NullableFloatList


class CreateRequestDTO(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    status: str = Field(..., pattern="^(new|in_progress|resolved|cancelled)$")
    category_id: int = Field(..., gt=0)
    assignee_id: int = Field(..., gt=0)


class SearchRequestDTO(BaseModel):
    embedding: NullableFloatList = None
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    limit: int = Field(default=5, gt=0, le=100)