from typing import Generic, TypeVar
from pydantic import BaseModel, Field

DataVar = TypeVar("DataVar")
ListItem = TypeVar("ListItem")


class ApiResponse(BaseModel, Generic[DataVar]):
    data: DataVar = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    meta: dict = Field(default_factory=dict)


class PaginatedResponse(BaseModel, Generic[ListItem]):
    items: list[ListItem] = Field(default_factory=list)
    total: int
    limit: int
    offset: int
