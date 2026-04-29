from app.schemas.users import UserCreate


def test_login(client):
    # register
    user = UserCreate(
        name="John",
        email="john@gmail.com",
        password="foobar",
    )
    client.post("/api/v1/users/register", json=user.model_dump())

    # login
    response = client.post(
        "/api/v1/users/login",
        data={"username": "john@gmail.com", "password": "foobar"},
    )
    assert response.status_code == 200


def test_create_note_without_authorization(client):
    response = client.post(
        "/api/v1/notes",
        json={"title": "test title", "content": "test content", "tags": []},
    )
    assert response.status_code == 401


def test_create_note_with_authorization(client_auth):
    response = client_auth.post(
        "/api/v1/notes",
        json={"title": "test title", "content": "test content", "tags": []},
    )
    assert response.status_code == 200


def test_get_note_without_authorization(client):
    response = client.get("/api/v1/notes/1")
    assert response.status_code == 401


def test_get_note_with_authorization(client_auth):
    response = client_auth.get("/api/v1/notes/1")
    assert response.status_code == 404  # meaning authorized, but note not found
