from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.services.auth import hash_password
from src.database.engine import AsyncSessionFactory
from src.users.models import User


class UserRepository:

    @staticmethod
    async def get_by_email(email: str, db: AsyncSession) -> User:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user
        
    @staticmethod
    async def get_by_uuid(uuid: str, db: AsyncSession) -> User:
        stmt = select(User).where(User.id == uuid)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user
        
    @staticmethod
    async def create(email: str, password: str, db: AsyncSession) -> User:
        hashed_password = hash_password(password)
        user = User(email=email, password=hashed_password)
        await user.save(db)
        return user