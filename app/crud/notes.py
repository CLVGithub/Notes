from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.notes import Note, Tag
from app.schemas.notes import Sort, Order

SORT_COLUMN_MAP = {
    Sort.created_at: Note.created_at,
    Sort.updated_at: Note.updated_at,
}


def create_note(db: Session, note_data, user_id: int):
    # notice the duck typing.  No Pydantic model is imported, Python just cares that the attributes exist on the note_data object
    note = Note(
        title=note_data.title,
        content=note_data.content,
        pinned=note_data.pinned,
        archived=note_data.archived,
        owner=user_id,
    )

    for tag_name in note_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()

        if not tag:
            tag = Tag(name=tag_name)

        note.tags.append(tag)

    db.add(note)
    db.commit()
    db.refresh(note)

    return note


def get_note(db: Session, note_id: int, user_id: int):
    stmt = select(Note).where(Note.owner == user_id).where(Note.id == note_id)
    note = db.scalars(stmt).first()
    return note


def get_all_notes(db: Session, user_id: int):
    stmt = select(Note).where(Note.owner == user_id)
    notes = db.scalars(stmt).all()
    return notes


# TODO: remove tags if they are no longer used by any note
def delete_note(db: Session, note_id: int, user_id: int):
    stmt = select(Note).where(Note.owner == user_id).where(Note.id == note_id)
    note = db.scalars(stmt).first()

    if note:
        db.delete(note)
        db.commit()

    return note


def update_note(db: Session, note_id: int, note_data, user_id: int):
    stmt = select(Note).where(Note.owner == user_id).where(Note.id == note_id)
    note = db.scalars(stmt).first()
    # note = db.get(Note, note_id)

    if note:
        note.title = note_data.title
        note.content = note_data.content

        note.tags.clear()
        for tag_name in note_data.tags:
            # If the tag already exists, dont recreate it
            tag = db.query(Tag).filter(Tag.name == tag_name).first()

            if not tag:
                tag = Tag(name=tag_name)

            note.tags.append(tag)

        note.pinned = note_data.pinned
        note.archived = note_data.archived

        db.commit()

    return note


def search_notes(
    db: Session, sort: Sort, order: Order, skip: int, limit: int, user_id: int
):
    stmt = select(Note).where(Note.owner == user_id).offset(skip).limit(limit)
    sort_column = SORT_COLUMN_MAP[sort]

    if order == Order.ascending:
        stmt = stmt.order_by(sort_column.asc())
    else:
        stmt = stmt.order_by(sort_column.desc())

    notes = db.execute(stmt).scalars().all()
    return notes
