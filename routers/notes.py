from fastapi import APIRouter, HTTPException
from models.notes import Note, Sort, NoteWithPassword

router = APIRouter(prefix="/notes", tags=["notes"])

items = [
    Note(
        title="Food",
        content="I love these kinds of foods",
        tags=["food", "health", "exercise"],
    ),
    Note(
        title="Study",
        content="Need to study these chapters.",
        tags=["university", "books"],
    ),
    Note(
        title="Laundry",
        content="These are the detergents to use and the method to follow.",
        tags=["chores", "clothes"],
    ),
]


@router.get(
    "/hello",
    summary="Say hello",
)
async def hello():
    """
    # Motivation
    Just your standard hello world response.  It will only return the words Hello World."""
    return "Hello World"


@router.get("/items/{item_id}")
async def get_item(item_id: int):
    return items[item_id]


@router.get("/search")
async def search(
    q: str, sort: Sort = Sort("updated_at"), skip: int = 0, limit: int = 2
):
    return {"query": q, "items": items[skip : skip + limit], "sort": sort}


@router.post("/", response_model=Note, tags=["notes"])
async def post_notes(note: Note):
    """This endpoint will only post a new note into the database with the data supplied by the request's body"""
    items.append(Note(title=note.title, content=note.content, tags=note.tags))
    return Note(title=note.title, content=note.content, tags=note.tags)


@router.get("/", tags=["notes"])
async def get_notes():
    return items


# class NoteResponse(BaseModel) #  It wanted a NoteResponse model, which just excludes internal fields.  It would set the response_model=NoteResponse field.
# I chose to use the inheritance model instead as it allows for editors not to complain about wrong return types


@router.get("/{id}", tags=["id"])
async def get_note_without_password(id: int) -> Note:
    """This will just return the note in the position of the list.

    It is supposed to eventually filter out unwanted attributes in the database in which the note resides."""

    if id >= len(items):
        raise HTTPException(
            status_code=404, detail=f"The note with ID {id} does not exist."
        )
    return items[id]


@router.put("/{id}", tags=["id"])  # , response_model=Note
async def put_note_without_password(note: NoteWithPassword, id: int) -> Note:
    """This will return the note sent without the password that was sent to it, to ensure that the password is filtered from the rest of the note.

    This is just to show an example of filtering out fields.

    This just illustrates that when you specify the return type to be a parent class without the password field, the password will be filtered out in the response."""

    if note.password == "wrongpassword":
        raise HTTPException(
            status_code=404, detail="You have supplied the wrong password."
        )
    if id >= len(items):
        raise HTTPException(
            status_code=404, detail=f"The note with ID {id} does not exist."
        )

    return note


@router.delete("/{id}", tags=["id"])
async def delete_note_without_password(id: int) -> Note:
    if id >= len(items):
        raise HTTPException(
            status_code=404, detail=f"The note with ID {id} does not exist."
        )
    return_note = items[id]
    items.pop(id)
    return return_note
