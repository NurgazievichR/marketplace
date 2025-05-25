from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession


from src.auth.schemas import UserRegister
from src.users.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)

async def register_user(user_data: UserRegister, db_session: AsyncSession):
    hashed_password = hash_password(user_data.password)
    user_dict = user_data.model_dump(exclude={'password', 'confirm_password'})
    user: User = User(**user_dict, password=hashed_password)
    print('here1')
    await user.save(db_session)
    return user

