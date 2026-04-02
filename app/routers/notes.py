from fastapi import APIRouter, HTTPException, Depends, status
from app.core.security import get_current_user
from app.schemas.notes import NoteCreate, NoteResponse, Sort, Order
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.crud import notes as crud_note
from app.models.users import User


router = APIRouter(prefix="/notes", tags=["notes"])


# create a note
@router.post("/", response_model=NoteResponse, summary="Put a note into the database")
async def create_note(
    note: NoteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud_note.create_note(db, note, user.id)


@router.get(
    "/search",
    response_model=List[NoteResponse],
    summary="Sort the notes according to dates, and paginate the sorted notes",
)
async def search(
    sort: Sort = Sort("updated_at"),
    order: Order = Order("ascending"),
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Searches for a range of notes.

    Once sorted according to created_at/updated_at dates in an ascending/descending fashion, it will skip an amount of notes from the first row and limit the amount of notes returned.
    """
    notes = crud_note.search_notes(db, sort, order, skip, limit, user.id)
    if not notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No notes within the search parameters could be found.",
        )
    return notes


# get a note
@router.get("/{note_id}", summary="Get a single note with a specific ID")
async def get_note(
    note_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    note = crud_note.get_note(db, note_id, user.id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The note with ID {note_id} could not be found.",
        )
    return note


# get all notes
@router.get(
    "/",
    response_model=List[NoteResponse],
    summary="Get all the notes for the current user",
)
async def get_all_notes(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    notes = crud_note.get_all_notes(db, user.id)
    if not notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No note could be found.",
        )
    return notes


# update a note
@router.put(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Update a note with a provided ID",
)
async def update_note(
    note_id: int,
    note_data: NoteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = crud_note.update_note(db, note_id, note_data, user.id)
    if not note:
        raise HTTPException(
            status_code=404, detail=f"The note with id {note_id} does not exist."
        )

    return note


# delete a note
@router.delete(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Delete a note with a provided ID",
)
async def delete_note(
    note_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    note = crud_note.delete_note(db, note_id, user.id)
    if note:
        return note
    else:
        raise HTTPException(
            status_code=404,
            detail=f"The note with id {note_id} does not exist.",
        )
