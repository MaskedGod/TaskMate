from typing import AsyncGenerator
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


async_engine = create_async_engine(url=settings.database_url)

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

metadata = MetaData()


class DatabaseSessionError(Exception):
    pass


class Base(DeclarativeBase):
    metadata = metadata


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise DatabaseSessionError(
            "An error occurred during the database session", e
        ) from e
    finally:
        await session.close()
