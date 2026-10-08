from pydantic import BaseModel, Field


class CreateRequestDTO(BaseModel):
    """DTO для создания или обновления заявки на обслуживание."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Краткое название неисправности (до 255 символов)",
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Подробное описание проблемы, включая наблюдаемые симптомы",
    )
    status: str = Field(
        ...,
        pattern="^(new|in_progress|resolved|cancelled)$",
        description="Текущий статус заявки: new, in_progress, resolved или cancelled",
    )
    category_id: int = Field(
        ...,
        gt=0,
        description="Идентификатор категории неисправности из справочника",
    )
    assignee_id: int = Field(
        ...,
        gt=0,
        description="Идентификатор сотрудника или отдела, ответственного за выполнение",
    )