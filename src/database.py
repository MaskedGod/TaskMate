from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings

async_engine = create_async_engine(url=settings.database_url)

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


class DatabaseSessionError(Exception):
    pass


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
