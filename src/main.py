from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI

from src.auth.routers import router as auth_router
from src.auth.exceptions import UserNotFoundError, handle_user_not_found
from src.database.engine import engine
from src.database.exceptions import (UniqueConstraintViolation,
                                     handle_unique_violation)
from src.redis import get_redis
from src.users.routers import router as users_router
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.redis = await get_redis(settings.redis_url)
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None) 
        yield  
    finally:
        await engine.dispose()
        await app.redis.aclose()


app = FastAPI(title='MarketPlace API', lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)

app.add_exception_handler(UniqueConstraintViolation, handle_unique_violation)
app.add_exception_handler(UserNotFoundError, handle_user_not_found)