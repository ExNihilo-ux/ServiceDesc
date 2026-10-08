# backend/app/schemas/requests/response.py
from datetime import datetime
from pydantic import BaseModel, Field


class RequestResponseDTO(BaseModel):
    """DTO для ответа при получении или создании заявки."""

    id: str = Field(
        ...,
        description="Уникальный идентификатор заявки (UUID v4)",
    )
    title: str = Field(
        ...,
        description="Краткое название неисправности",
    )
    description: str = Field(
        ...,
        description="Подробное описание проблемы и наблюдаемых симптомов",
    )
    status: str = Field(
        ...,
        description="Текущий статус заявки (new, in_progress, resolved, cancelled)",
    )
    category_id: int = Field(
        ...,
        description="Идентификатор категории неисправности из справочника",
    )
    assignee_id: int = Field(
        ...,
        description="Идентификатор сотрудника или отдела, ответственного за выполнение",
    )
    created_at: datetime = Field(
        ...,
        description="Дата и время создания заявки в формате ISO 8601",
    )