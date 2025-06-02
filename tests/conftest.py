from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import settings
from src.database.base import Base
from src.database.engine import get_db
from src.database.engine import get_db as original_get_db
from src.main import app

TEST_DB_URL = settings.postgres_url_test

engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def override_get_db():
    async with AsyncSessionFactory() as session:
        yield session

app.dependency_overrides[original_get_db] = override_get_db

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app) 
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client