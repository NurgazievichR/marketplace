import redis.asyncio as redis
from src.config import settings


async def get_redis() -> redis.Redis:
    return await redis.from_url(
        settings.redis_url,
        encoding = 'utf-8',
        decode_responses = True
    )
