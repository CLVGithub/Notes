from fastapi import APIRouter, HTTPException, Depends
from app.schemas.notes import NoteCreate, NoteResponse, Sort, Order
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.crud import notes as crud_note

router = APIRouter(prefix="/notes", tags=["notes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create a note
@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return crud_note.create_note(db, note)


@router.get("/search", response_model=List[NoteResponse])
async def search(
    sort: Sort = Sort("updated_at"),
    order: Order = Order("ascending"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Searches for a range of notes.

    Once sorted according to created_at/updated_at dates in an ascending/descending fashion, will skip an amount of notes from the first row and limit the amount of notes returned.
    """
    notes = crud_note.search_notes(db, sort, order, skip, limit)
    return notes


# get a note
@router.get("/{note_id}")
async def get_note(note_id: int, db: Session = Depends(get_db)):
    return crud_note.get_note(db, note_id)


# get all notes
@router.get("/", response_model=List[NoteResponse])
async def get_all_notes(db: Session = Depends(get_db)):
    return crud_note.get_all_notes(db)


# update a note
@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int, note_data: NoteCreate, db: Session = Depends(get_db)
):
    note = crud_note.update_note(db, note_id, note_data)
    if not note:
        raise HTTPException(
            status_code=404, detail=f"The note with id {note_id} does not exist."
        )

    return note


# delete a note
@router.delete("/{note_id}", response_model=NoteResponse)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = crud_note.delete_note(db, note_id)
    if note:
        return note
    else:
        raise HTTPException(
            status_code=404, detail=f"The note with id {note_id} does not exist."
        )


# @router.put("/", tags=["id"])  # , response_model=Note
# async def put_note_without_password(note: NoteWithPassword, id: int) -> Note:
#     """This will return the note sent without the password that was sent to it, to ensure that the password is filtered from the rest of the note.
#
#     This is just to show an example of filtering out fields.
#
#     This just illustrates that when you specify the return type to be a parent class without the password field, the password will be filtered out in the response."""
#
#     if note.password == "wrongpassword":
#         raise HTTPException(
#             status_code=404, detail="You have supplied the wrong password."
#         )
#     if id >= len(items):
#         raise HTTPException(
#             status_code=404, detail=f"The note with ID {id} does not exist."
#         )
#
#     return note
