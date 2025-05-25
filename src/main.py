from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None) 
        yield  
    finally:
        await engine.dispose()


app = FastAPI(title='MarketPlace API', lifespan=lifespan)

