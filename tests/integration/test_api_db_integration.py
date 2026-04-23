from app.core.security import create_access_token

# Spongebob
# spongebob@gmail.com
# password: gary
#
# Sandy
# sandy@gmail.com
# password: cheeks


def test_create_note_with_authorization(client):
    response = client.post(
        "/api/v1/users/register",
        json={"name": "Spongebob", "email": "spongebob@gmail.com", "password": "gary"},
    )
    assert response.status_code == 200

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "spongebob@gmail.com",
            "password": "gary",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/notes",
        json={"title": "test title", "content": "test content", "tags": []},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "test title"
    assert response.json()["content"] == "test content"


def test_sandy_user(client, sample_user):
    # response = client.
    pass
