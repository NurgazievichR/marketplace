from fastapi import APIRouter, Depends, Request
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserRegisterSchema, UserLoginSchema, RefreshTokenSchema, TokenPairSchema
from src.auth.services.auth import create_user, get_token_pair, authenticate_user, get_user, set_user_session_redis, get_payload
from src.database.engine import get_db

router = APIRouter(prefix='/auth', tags=['Авторизация'])

@router.post('/register', summary='Регистрация')
async def register(request: Request, user_data: UserRegisterSchema, db_session: Annotated[AsyncSession, Depends(get_db)]) -> TokenPairSchema:
    user = await create_user(user_data, db_session)
    token_pair = get_token_pair(user)
    set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair

@router.post('/login', summary='Логин')
async def login(request: Request, user_data: UserLoginSchema, db_session: Annotated[AsyncSession, Depends(get_db)]) -> TokenPairSchema:
    user = await authenticate_user(user_data, db_session)
    token_pair = get_token_pair(user)
    set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair

@router.post('/refresh', summary='Получить refresh token')
async def refresh(request: Request, refresh_token: RefreshTokenSchema) -> TokenPairSchema:
    payload = get_payload(refresh_token.refresh_token)
    user = get_user(payload['id'])
    token_pair = get_token_pair(user)
    set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair