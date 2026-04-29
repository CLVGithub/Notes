from app.crud.notes import create_note
from app.schemas.notes import NoteCreate
from app.models.notes import Note


def test_create_note(get_test_db):
    note = NoteCreate(
        title="title",
        content="content",
        tags=["tag1", "tag2"],
        pinned=False,
        archived=False,
    )
    response = create_note(get_test_db, note, 1)

    assert response.title == "title"
    assert response.content == "content"
    tag_names = [tag.name for tag in response.tags]
    assert tag_names == ["tag1", "tag2"]
    assert response.pinned is False
    assert response.archived is False
