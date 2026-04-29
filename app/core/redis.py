import os
import redis

REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL is None:
    raise ValueError("REDIS_URL is not set")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
