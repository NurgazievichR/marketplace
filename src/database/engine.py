from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

DATABASE_URL = settings.postgres_url

engine = create_async_engine(
    DATABASE_URL,
    future=True, # переход на sqlalchemy 2.0
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
