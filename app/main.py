from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import engine, Base
from app.routers.notes import router as notes_router
import app.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("CREATING TABLES")
    print(Base.metadata.tables.keys())
    # Startup code
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown code
    # close connections, cleanup, etc.


app = FastAPI(title="Notes API", lifespan=lifespan)
app.include_router(notes_router)

if __name__ == "__main__":
    print("inside the condition")
