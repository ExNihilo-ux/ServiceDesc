from pydantic import BaseModel, Field

from app.schemas.types import NullableFloatList


class SearchRequestDTO(BaseModel):
    """DTO для векторного поиска похожих заявок."""
    embedding: NullableFloatList = None
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    limit: int = Field(default=5, gt=0, le=100)