from fastapi import APIRouter, Depends
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