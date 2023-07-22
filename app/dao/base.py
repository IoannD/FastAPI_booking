from typing import List
from app.database import async_session_maker
from sqlalchemy import select, insert, delete


class BaseDAO():
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod  # for access method as BookingDAO.find_all()
    async def find_all(cls, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        query = insert(cls.model).values(**data)
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()
