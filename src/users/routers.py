import json

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.engine import get_db
from src.users.models import User
from src.users.schemas import UserPublicSchema

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/", response_model=list[UserPublicSchema])
async def list_users(db_session: AsyncSession = Depends(get_db)):
    result = await db_session.execute(select(User))
    users = result.scalars().all()
    return users

@router.delete("/")
async def clear_users_table(db_session: AsyncSession = Depends(get_db)):
    try:
        await db_session.execute(delete(User))
        await db_session.commit()
        return {"detail": "User table cleared."}
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear users: {str(e)}")

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

@router.delete("/redis")
async def clear_redis(request: Request):
    redis = request.app.redis
    await redis.flushdb()
    return {"detail": "Redis database cleared."}