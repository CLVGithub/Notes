from pydantic import BaseModel
from enum import Enum


class Note(BaseModel):
    title: str
    content: str
    tags: list[str]
    pinned: bool | None = None
    archived: bool | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    # FIX:  figure out how to send the tags in the response's body
    # tags: list[str]
    # # created_at try to implement to see
    pinned: bool | None = None
    archived: bool | None = None

    class Config:
        from_attributes = True


class NoteWithPassword(Note):
    password: str


class Sort(str, Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class Order(str, Enum):
    ascending = "ascending"
    descending = "descending"
