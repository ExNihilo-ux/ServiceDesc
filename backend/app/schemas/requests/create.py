from pydantic import BaseModel, Field


class CreateRequestDTO(BaseModel):
    """DTO для создания/обновления заявки."""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    status: str = Field(..., pattern="^(new|in_progress|resolved|cancelled)$")
    category_id: int = Field(..., gt=0)
    assignee_id: int = Field(..., gt=0)