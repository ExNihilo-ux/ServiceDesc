from pydantic import BaseModel, Field

from app.schemas.types import NullableFloatList


class SearchRequestDTO(BaseModel):
    """DTO для векторного поиска похожих заявок."""

    embedding: NullableFloatList = Field(
        default=None,
        description="Векторное представление текста заявки (список float). Если null, поиск не выполняется",
    )
    threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Минимальный порог косинусного сходства (от 0.0 до 1.0). Чем выше значение, тем строже поиск",
    )
    limit: int = Field(
        default=5,
        gt=0,
        le=100,
        description="Максимальное количество возвращаемых результатов (не более 100)",
    )