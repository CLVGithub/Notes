import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.core.database import get_db
from tests.database import TestingSessionLocal, init_test_db, drop_test_db


# Create a fresh DB for the whole test session
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_test_db()
    yield
    drop_test_db()


# Create a new DB session for each test
@pytest.fixture()
def get_test_db():
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()


# Override FastAPI dependency
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
