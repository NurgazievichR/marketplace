import redis.asyncio as redis


async def get_redis(redis_url) -> redis.Redis:
    return await redis.from_url(
        redis_url,
        encoding = 'utf-8',
        decode_responses = True
    )
