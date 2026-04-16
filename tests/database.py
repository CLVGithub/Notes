from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_test_db():
    Base.metadata.create_all(bind=engine)


def drop_test_db():
    Base.metadata.drop_all(bind=engine)
