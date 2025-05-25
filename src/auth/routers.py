from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserRegister
from src.auth.services.auth import register_user
from src.database.engine import get_db



router = APIRouter(prefix='/auth', tags=['Авторизация'])


@router.post('/register')
async def register(user_data: UserRegister, db_session: Annotated[AsyncSession, Depends(get_db)]):
    user = await register_user(user_data, db_session)
    return {'message': 'success'}