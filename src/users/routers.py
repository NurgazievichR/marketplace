from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.engine import get_db
from src.users.models import User
from src.users.schemas import UserPublicSchema 

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/", response_model=list[UserPublicSchema])
async def list_users(db_session: AsyncSession = Depends(get_db)):
    result = await db_session.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/redis")
async def get_all_redis_data(request: Request):
    redis = request.app.redis 
    keys = await redis.keys("*")

    if not keys:
        return {}

    result = {}
    for key in keys:
        value = await redis.get(key)
        result[key] = value

    return result