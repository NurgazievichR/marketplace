from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from datetime import datetime, timezone, timedelta

from src.auth.schemas import UserRegister, LoginForm, TokenPair
from src.users.models import User
from src.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)

async def create_user(user_data: UserRegister, db_session: AsyncSession) -> User:
    hashed_password = hash_password(user_data.password)
    user_dict = user_data.model_dump(exclude={'password', 'confirm_password'})
    user: User = User(**user_dict, password=hashed_password)
    await user.save(db_session)
    return user
    
async def authenticate_user(user_data: LoginForm, db_session: AsyncSession) -> User:
    stmt = select(User).where(User.email == user_data.email)
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_token_pair(user: User) -> TokenPair:
    now = datetime.now(timezone.utc)

    access_payload = {
        'sub': str(user.id),
        'exp': now + timedelta(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        'type': 'access'
    }

    access_exclueded_data = ('password', 'id')
    for k,v in user.__dict__.items():
        if not k.startswith('_') and k not in access_exclueded_data:
            access_payload[k] = v

    refresh_payload = {
        'sub': str(user.id),
        'exp': now + timedelta(settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        'type': 'refresh'
    }

    access = jwt.encode(access_payload, **settings.get_auth_data)
    refresh = jwt.encode(refresh_payload, **settings.get_auth_data)

    token_pair = TokenPair(access_token=access, refresh_token=refresh)
    return token_pair

