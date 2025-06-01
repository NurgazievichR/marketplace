import json
import redis.asyncio as redis

from src.auth.schemas import TokenPairSchema
from src.config import settings

async def set_user_session_redis(redis:redis.Redis, token_pair: TokenPairSchema, user_email: str):
    key = f"user:{user_email}"
    value = token_pair.model_dump(exclude=['token_type'])
    await redis.set(
        key,
        json.dumps(value),
        ex=settings.JWT_REFRESH_TOKEN_EXPIRE
    )