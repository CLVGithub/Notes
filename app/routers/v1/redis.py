from fastapi import APIRouter
from app.core.redis import redis_client

router = APIRouter(prefix="/api/v1/redis", tags=["redis"])


@router.post("/")
async def cache_data():
    redis_client.set("test_key", "hello")
    return {"Value successfully stored in cache"}


@router.get("/")
async def retrieve_data():
    value = redis_client.get("test_key")
    return {"value": value}
