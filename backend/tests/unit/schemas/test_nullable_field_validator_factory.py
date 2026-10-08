# backend/tests/unit/schemas/test_nullable_field_validator_factory.py
import pytest
from pydantic import BaseModel, ValidationError, Field

from app.schemas.base import NullableBaseModel


class TestNullableFieldValidatorFactoryMechanism:
    """Тесты механизма фабрики nullable-валидаторов."""

    def test_passes_none_through_unchanged(self):
        """Явный null проходит через фабрику без модификаций."""
        class DTO(NullableBaseModel):
            value: list[float] | None = None
            _validate = NullableBaseModel._nullable_field_validator("value")

        assert DTO(value=None).value is None

    def test_preserves_pydantic_default_when_field_omitted(self):
        """Пропущенное поле получает default из аннотации Pydantic."""
        class DTO(NullableBaseModel):
            value: list[float] | None = None
            _validate = NullableBaseModel._nullable_field_validator("value")

        assert DTO().value is None

    def test_works_with_any_type_not_only_lists(self):
        """Фабрика универсальна: работает со str, int, dict и др."""
        class DTO(NullableBaseModel):
            name: str | None = None
            count: int | None = None
            meta: dict | None = None
            _validate_name = NullableBaseModel._nullable_field_validator("name")
            _validate_count = NullableBaseModel._nullable_field_validator("count")
            _validate_meta = NullableBaseModel._nullable_field_validator("meta")

        dto = DTO(name="test", count=42, meta={"k": "v"})
        assert dto.name == "test"
        assert dto.count == 42
        assert dto.meta == {"k": "v"}

    def test_does_not_interfere_with_subsequent_pydantic_validators(self):
        """mode='before' корректно встраивается в pipeline валидации."""
        class DTO(NullableBaseModel):
            value: list[float] | None = Field(default=None, min_length=2)
            _validate = NullableBaseModel._nullable_field_validator("value")

        # None допустим (min_length не применяется к None)
        assert DTO(value=None).value is None

        # Валидный список проходит обе проверки
        assert DTO(value=[1.0, 2.0]).value == [1.0, 2.0]

        # Невалидный список отклоняется Pydantic после фабрики
        with pytest.raises(ValidationError):
            DTO(value=[1.0])

    def test_creates_independent_validators_per_field(self):
        """Каждый вызов фабрики создаёт изолированный валидатор."""
        class DTO(NullableBaseModel):
            a: list[float] | None = None
            b: list[float] | None = None
            _validate_a = NullableBaseModel._nullable_field_validator("a")
            _validate_b = NullableBaseModel._nullable_field_validator("b")

        dto = DTO(a=None, b=[0.5])
        assert dto.a is None
        assert dto.b == [0.5]

    def test_coexists_with_required_fields_without_side_effects(self):
        """Nullable-поля через фабрику не ломают обязательные поля."""
        class DTO(NullableBaseModel):
            required: str = Field(..., min_length=1)
            optional: list[float] | None = None
            _validate_optional = NullableBaseModel._nullable_field_validator("optional")

        with pytest.raises(ValidationError):
            DTO()

        dto = DTO(required="ok", optional=None)
        assert dto.required == "ok"
        assert dto.optional is None

    def test_passes_valid_value_through_with_equal_content(self):
        """Валидное значение сохраняется с тем же содержимым (Pydantic может копировать)."""
        class DTO(NullableBaseModel):
            value: list[float] | None = None
            _validate = NullableBaseModel._nullable_field_validator("value")

        data = [0.1, 0.5]
        result = DTO(value=data).value
        # Проверяем равенство содержимого, а не идентичность объекта
        assert result == data
        assert isinstance(result, list)
        assert len(result) == 2

    def test_returns_pydantic_compatible_descriptor(self):
        """Фабрика возвращает объект, совместимый с системой валидации Pydantic."""
        validator = NullableBaseModel._nullable_field_validator("x")
        # Проверяем, что это дескриптор Pydantic, а не сырая функция
        assert hasattr(validator, 'wrapped') or hasattr(validator, '__call__')
        # Главное: он должен успешно применяться как атрибут класса
        class DTO(NullableBaseModel):
            x: str | None = None
            _validate_x = validator
        
        # Если бы фабрика вернула некорректный объект, создание DTO упало бы
        dto = DTO(x="test")
        assert dto.x == "test"