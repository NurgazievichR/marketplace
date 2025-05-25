from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.engine import engine

from src.auth.routers import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None) 
        yield  
    finally:
        await engine.dispose()


app = FastAPI(title='MarketPlace API', lifespan=lifespan)
app.include_router(auth_router)

