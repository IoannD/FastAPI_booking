from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


if settings.MODE == 'TEST':
    database_url = settings.get_test_database_utl
    database_params = {'poolclass': NullPool}
else:
    database_url = settings.get_database_utl
    database_params = {}

engine = create_async_engine(database_url, **database_params)

async_session_maker = sessionmaker(engine, class_=AsyncSession,
                                   expire_on_commit=False)


class Base(DeclarativeBase):
    pass
