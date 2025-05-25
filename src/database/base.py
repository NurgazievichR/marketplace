from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    async def save(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=repr(e)) from e

    async def delete(self, db_session: AsyncSession):
        try:
            await db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=repr(e)) from e

    async def update(self, db_session: AsyncSession, **kwargs):
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            await db_session.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=repr(e)) from e

    async def save_or_update(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.commit()
        except IntegrityError as e:
            if isinstance(e.orig, UniqueViolationError):
                return await db_session.merge(self)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=repr(e)) from e
