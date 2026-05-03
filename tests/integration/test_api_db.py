def test_user_creation(client):
    response = client.post(
        "/api/v1/users/register",
        json={"name": "Spongebob", "email": "spongebob@gmail.com", "password": "gary"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.post(
        "/api/v1/users/register",
        json={"name": "Sandy", "email": "sandy@gmail.com", "password": "cheeks"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == 2


def test_double_user_creation(client):
    response = client.post(
        "/api/v1/users/register",
        json={"name": "Spongebob", "email": "spongebob@gmail.com", "password": "gary"},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/users/register",
        json={"name": "Spongebob", "email": "spongebob@gmail.com", "password": "gary"},
    )
    assert response.status_code == 409


def test_note_manipulations_with_authorization(client):
    # Create the user
    response = client.post(
        "/api/v1/users/register",
        json={"name": "Spongebob", "email": "spongebob@gmail.com", "password": "gary"},
    )
    assert response.status_code == 200

    # Login the user and get JWT token
    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "spongebob@gmail.com",
            "password": "gary",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Create the note for the logged in user
    response = client.post(
        "/api/v1/notes",
        json={"title": "test title", "content": "test content", "tags": []},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "test title"
    assert response.json()["content"] == "test content"
    assert response.json()["id"] == 1

    # Retrieve the note for the logged in user
    response = client.get(
        "/api/v1/notes/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json()["id"] == 1
    assert response.json()["owner"] == 1
    assert response.json()["title"] == "test title"
    assert response.json()["content"] == "test content"
    assert response.json()["tags"] == []

    # Delete the note
    response = client.delete(
        "/api/v1/notes/1",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    # print(response.json())
    assert response.json()["id"] == 1
    assert response.json()["owner"] == 1
    assert response.json()["title"] == "test title"
    assert response.json()["content"] == "test content"


# TODO: Run pytest in Docker containers
