from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.database.exceptions import UniqueConstraintViolation


class Base(DeclarativeBase):
    async def _raise_with_rollback(self, db_session:AsyncSession, e:Exception):
        await db_session.rollback() #вернуться в исходную при исключении
        if isinstance(e, IntegrityError):
            raise UniqueConstraintViolation(e)

        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(e)) 

    async def save(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.commit()
            await db_session.refresh(self) 
        except SQLAlchemyError as e:
            await self._raise_with_rollback(db_session, e)

    async def delete(self, db_session: AsyncSession):
        try:    
            await db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as e:
            await self._raise_with_rollback(db_session, e)

    async def update(self, db_session: AsyncSession, **kwargs):
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            await db_session.commit()
        except SQLAlchemyError as e:
            await self._raise_with_rollback(db_session, e)

    async def save_or_update(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.commit()
            await db_session.refresh(self)
        except IntegrityError as e:
            await db_session.rollback()
            if isinstance(e.orig, UniqueViolationError):
                await db_session.merge(self)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=repr(e)) from e
