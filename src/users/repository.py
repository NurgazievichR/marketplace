from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.users.models import User
from src.database.engine import AsyncSessionFactory
from src.auth.services.auth import hash_password

class UserRepository:

    @staticmethod
    async def get_by_email(email: str) -> User:
        async with AsyncSessionFactory() as db:
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            return user
        
    @staticmethod
    async def get_by_uuid(uuid: str) -> User:
        async with AsyncSessionFactory() as db:
            stmt = select(User).where(User.id == uuid)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            return user
        
    @staticmethod
    async def create(email: str, password: str) -> User:
        async with AsyncSessionFactory() as db:
            hashed_password = hash_password(password)
            user = User(email=email, password=hashed_password)
            await user.save(db)
            return user