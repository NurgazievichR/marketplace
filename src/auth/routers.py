from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserRegister, LoginForm, TokenPair
from src.auth.services.auth import create_user, get_token_pair, authenticate_user
from src.database.engine import get_db

router = APIRouter(prefix='/auth', tags=['Авторизация'])

@router.post('/register', summary='Регистрация')
async def register(user_data: UserRegister, db_session: Annotated[AsyncSession, Depends(get_db)]) -> TokenPair:
    user = await create_user(user_data, db_session)
    token_pair = get_token_pair(user)
    return token_pair

@router.post('/login', summary='Логин')
async def login(user_data: LoginForm, db_session: Annotated[AsyncSession, Depends(get_db)]) -> TokenPair:
    user = await authenticate_user(user_data, db_session)
    token_pair = get_token_pair(user)
    return token_pair