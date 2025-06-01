from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.engine import engine
from src.redis import get_redis

from src.auth.routers import router as auth_router
from src.users.routers import router as users_router

from src.database.exceptions import UniqueConstraintViolation, handle_unique_violation

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.redis = await get_redis()
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None) 
        yield  
    finally:
        await engine.dispose()
        await app.redis.close()


app = FastAPI(title='MarketPlace API', lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)

app.add_exception_handler(UniqueConstraintViolation, handle_unique_violation)
