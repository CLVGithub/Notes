from pydantic import BaseModel, ConfigDict
from enum import Enum


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str]
    pinned: bool = False
    archived: bool = False


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    pinned: bool = False
    archived: bool = False
    owner: int

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)


class Sort(str, Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class Order(str, Enum):
    ascending = "ascending"
    descending = "descending"
