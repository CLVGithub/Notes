from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test", override=True)  # Load test environment variables
# Environment variables are set before test modules are imported

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.core.database import get_db
from tests.database import TestingSessionLocal, init_test_db, drop_test_db, engine

# these imports are to set up rows in the test database
from app.models.notes import Note
from app.schemas.users import UserCreate
from app.schemas.notes import NoteCreate
from app.crud.users import create_user
from app.crud.notes import create_note

from app.models.users import User
from app.core.security import get_current_user, hash_password


# Create a fresh DB for the whole test session
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_test_db()
    yield
    drop_test_db()


# Create a new DB session for each test
@pytest.fixture()
def get_test_db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# FastAPI client with test DB
@pytest.fixture()
def client(get_test_db):
    app = create_app()

    def override_get_db():
        try:
            yield get_test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)


# FastAPI client with mocked get_current_user
@pytest.fixture()
def client_auth(get_test_db):
    app = create_app()

    def override_get_db():
        try:
            yield get_test_db
        finally:
            pass

    def override_get_current_user():
        return User(
            id=1,
            name="Fake User",
            email="fakeuser@gmail.com",
            hashed_password=hash_password("password"),
        )

    app.dependency_overrides[get_db] = override_get_db
    # this bypasses giving a JWT token
    app.dependency_overrides[get_current_user] = override_get_current_user

    return TestClient(app)
