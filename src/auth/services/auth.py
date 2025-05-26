from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from datetime import datetime, timezone, timedelta
import redis.asyncio as redis
import json

from src.auth.schemas import UserRegisterSchema, UserLoginSchema, TokenPairSchema
from src.users.models import User
from src.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_payload(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid token claims")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or credentials.scheme.lower() != "bearer":
            raise HTTPException(status_code=403, detail="Invalid auth scheme.")

        token = credentials.credentials

        payload = get_payload(token)

async def get_user(email: str, db_session: AsyncSession) -> User:
    stmt = select(User).where(User.email == email)
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def create_user(user_data: UserRegisterSchema, db_session: AsyncSession) -> User:
    hashed_password = hash_password(user_data.password)
    user_dict = user_data.model_dump(exclude={'password', 'confirm_password'})
    user: User = User(**user_dict, password=hashed_password)
    await user.save(db_session)
    return user

async def authenticate_user(user_data: UserLoginSchema, db_session: AsyncSession) -> User:
    user = await get_user(user_data.email, db_session)
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Password is wrong")
    return user

def get_token_pair(user: User) -> TokenPairSchema:
    now = datetime.now(timezone.utc)

    access_payload = {
        'sub': str(user.id),
        'exp': now + timedelta(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        'type': 'access',
    }

    access_exclueded_data = ('password', 'id')
    for k,v in user.__dict__.items():
        if not k.startswith('_') and k not in access_exclueded_data:
            access_payload[k] = v

    refresh_payload = {
        'sub': str(user.id),
        'exp': now + timedelta(settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        'type': 'refresh',
        'email': user.email
    }

    access = jwt.encode(access_payload, **settings.get_auth_data)
    refresh = jwt.encode(refresh_payload, **settings.get_auth_data)

    token_pair = TokenPairSchema(access_token=access, refresh_token=refresh)
    return token_pair

async def set_user_session_redis(redis:redis.Redis, token_pair: TokenPairSchema, user_email: str):
    key = f"user:{user_email}"
    value = token_pair.model_dump(exclude=['token_type'])
    await redis.set(
        key,
        json.dumps(value),
        ex=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24
    )

    