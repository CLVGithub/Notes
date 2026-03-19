from pydantic import BaseModel
from enum import Enum


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: list[str]
    pinned: bool = False
    archived: bool = False
    owner_id: int


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    # FIX:  figure out how to send the tags in the response's body
    # tags: list[str]
    # # created_at try to implement to see
    pinned: bool = False
    archived: bool = False
    owner: int

    class Config:
        from_attributes = True


class NoteWithPassword(NoteCreate):
    password: str


class Sort(str, Enum):
    created_at = "created_at"
    updated_at = "updated_at"


class Order(str, Enum):
    ascending = "ascending"
    descending = "descending"
