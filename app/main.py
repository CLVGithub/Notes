from fastapi import FastAPI

from app.routers.v1.notes import router as notes_router
from app.routers.v1.tags import router as tags_router
from app.routers.v1.users import router as users_router
from app.routers.v1.redis import router as redis_router


def create_app():
    app = FastAPI(title="Notes API")

    app.include_router(notes_router)
    app.include_router(tags_router)
    app.include_router(users_router)
    app.include_router(redis_router)

    return app


app = create_app()
