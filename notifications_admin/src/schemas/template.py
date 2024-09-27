import re
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, model_validator, Field, ConfigDict, UUID4


class TypeEnum(StrEnum):

    email = "email"
    sms = "sms"
    push = "push"


class TemplateBase(BaseModel):
    """Базовая схема Шаблона"""

    name: str = Field(max_length=256)
    type: TypeEnum | None
    subject: str | None = Field(None, max_length=256)
    content: str
    parameters: list[str]


class TemplateCreateOrUpdate(TemplateBase):
    """Схема создания Шаблона"""

    @model_validator(mode="after")
    def check_subject(self):
        if self.type == TypeEnum.email and self.subject is None:
            raise ValueError(f"Subject is required for {self.type} template")

        return self

    @model_validator(mode="after")
    def check_content(self):
        if self.type != TypeEnum.email and re.search(
            r"<[^<>]+>", self.content
        ):
            raise ValueError(
                "Content must not contain html tags "
                f"for {self.type} template"
            )

        return self

    @model_validator(mode="after")
    def check_parameters(self):
        if len(self.parameters) > 0:
            if set(self.parameters) - set(self.content.split('%')):
                raise ValueError(
                    "All parameters must be in content "
                )

        return self


class TemplateDB(TemplateBase):
    """Схема получения Шаблона"""

    id: UUID4
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TemplateFilters(BaseModel):
    """Фильтры для получения Шаблонов"""

    type: TypeEnum | None = None
    page: int = Field(1, ge=1)
    per_page: int = Field(20, ge=1)


class TemplateMulti(BaseModel):

    templates: list[TemplateDB]
    total: int
    page: int
    per_page: int
