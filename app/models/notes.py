from sqlalchemy import ForeignKey, String, DateTime, func, Column, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.core.database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    pinned: Mapped[bool] = mapped_column(default=False)
    archived: Mapped[bool] = mapped_column(default=False)

    tags: Mapped[List["Tag"]] = relationship(
        secondary="note_tags",
        back_populates="notes",
        lazy="selectin",
    )

    owner: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, title={self.title!r}, content={self.content!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r}, pinned={self.pinned}, archived={self.archived}), tags={self.tags}"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    notes: Mapped[List["Note"]] = relationship(
        secondary="note_tags",
        back_populates="tags",
        lazy="selectin",
    )
    # TODO: create __repr__ methods


note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    # TODO: add ondelete "cascade" here.
)
