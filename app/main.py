from fastapi import FastAPI

from app.routers.v1.notes import router as notes_router
from app.routers.v1.tags import router as tags_router
from app.routers.v1.users import router as users_router

app = FastAPI(title="Notes API")

app.include_router(notes_router)
app.include_router(tags_router)
app.include_router(users_router)
