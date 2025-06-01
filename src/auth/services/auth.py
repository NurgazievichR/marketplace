from fastapi import HTTPException
from passlib.context import CryptContext

from src.auth.schemas import UserLoginSchema
from src.users.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(user_in: UserLoginSchema, user_db: User) -> None:
    if not verify_password(user_in.password, user_db.password):
        raise HTTPException(status_code=401, detail="Password is wrong")



    




