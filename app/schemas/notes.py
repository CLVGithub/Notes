from pydantic import BaseModel
from enum import Enum


class Note(BaseModel):
    title: str
    content: str
    tags: list[str]


class NoteWithPassword(Note):
    password: str


class Sort(str, Enum):
    created_at = "created_at"
    updated_at = "updated_at"
