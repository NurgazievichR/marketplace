from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import (RefreshTokenSchema, TokenPairSchema,
                              UserLoginSchema, UserRegisterSchema)
from src.auth.services import (authenticate_user, get_payload, get_token_pair,
                               set_user_session_redis)
from src.database.engine import get_db
from src.users.repository import UserRepository

router = APIRouter(prefix='/auth', tags=['Авторизация'])

@router.post('/register', summary='Регистрация')
async def register(request: Request, user_data: UserRegisterSchema) -> TokenPairSchema:
    user = await UserRepository.create(**user_data.model_dump(exclude=['confirm_password']))
    token_pair = get_token_pair(user)
    await set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair

@router.post('/login', summary='Логин')
async def login(request: Request, user_in: UserLoginSchema) -> TokenPairSchema:
    user = UserRepository.get_by_email(user_in.email)
    await authenticate_user(user_in, user)
    token_pair = get_token_pair(user)
    await set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair

@router.post('/refresh', summary='Получить refresh token')
async def refresh(request: Request, refresh_token: RefreshTokenSchema) -> TokenPairSchema:
    payload = get_payload(refresh_token.refresh_token)
    user = await UserRepository.get_by_email(payload['email'])
    token_pair = get_token_pair(user)
    await set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair