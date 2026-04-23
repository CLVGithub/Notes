from app.schemas.users import UserCreate


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"somekey": "This is the root"}


def test_login(client):
    user = UserCreate(
        name="John",
        email="john@gmail.com",
        password="foobar",
    )
    client.post("/api/v1/users/register", json=user.model_dump())
    response = client.post(
        "/api/v1/users/login",
        data={"username": "john@gmail.com", "password": "foobar"},
    )
    assert response.status_code == 200


def test_create_note_without_authorization(client):
    response = client.post("/api/v1/notes")
    assert response.status_code == 401


def test_get_note_without_authorization(client):
    response = client.get("/api/v1/notes")
    assert response.status_code == 401


# def test_get_note_with_authorization(client):
# setup a db first that is already ready
# TODO: It must be a good idea to have a base database with values already inserted in it that you can continually conjure up in your tests.  It must probably be some kind of fixture that can be supplied
# to the testing function, and after the testing function is complete, the database is unaffected between tests.  No commits were made to the database between tests.
