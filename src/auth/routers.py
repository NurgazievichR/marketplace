from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import UserNotFoundError
from src.auth.schemas import (RefreshTokenSchema, TokenPairSchema,
                              UserLoginSchema, UserRegisterSchema)
from src.auth.services import (authenticate_user, get_payload, get_token_pair,
                               set_user_session_redis)
from src.database.engine import get_db
from src.users.repository import UserRepository

from jose.exceptions import JWTClaimsError

router = APIRouter(prefix='/auth', tags=['Авторизация'])

@router.post('/register', summary='Регистрация')
async def register(request: Request, user_data: UserRegisterSchema, db_session: Annotated[AsyncSession, Depends(get_db)]) -> TokenPairSchema:
    user = await UserRepository.create(**user_data.model_dump(exclude=['confirm_password']), db=db_session)
    token_pair = get_token_pair(user)
    await set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair

@router.post('/login', summary='Логин')
async def login(request: Request, user_in: UserLoginSchema, db_session: Annotated[AsyncSession, Depends(get_db)]) -> TokenPairSchema:
    user = await UserRepository.get_by_email(user_in.email, db_session)
    if not user:
        raise UserNotFoundError(user_in.email)
    authenticate_user(user_in, user)
    token_pair = get_token_pair(user)
    await set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair

@router.post('/refresh', summary='Получить refresh token')
async def refresh(request: Request, refresh_token: RefreshTokenSchema, db_session: Annotated[AsyncSession, Depends(get_db)]) -> TokenPairSchema:
    payload = get_payload(refresh_token.refresh_token)
    user = await UserRepository.get_by_uuid(payload['sub'], db_session)
    token_pair = get_token_pair(user)
    await set_user_session_redis(request.app.redis, token_pair, user.email)
    return token_pair