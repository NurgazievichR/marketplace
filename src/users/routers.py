from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

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
async def get_users_from_redis(request: Request):
    redis = request.app.redis
    keys = await redis.keys("user:*")

    if not keys:
        raise HTTPException(status_code=404, detail="No user data in Redis")

    result = {}

    for key in keys:
        raw = await redis.get(key)
        try:
            result[key] = json.loads(raw)
        except Exception:
            result[key] = raw 

    return result