from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from . import models
from . import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


async def create_user(
    user_data: schemas.UserCreate, session: AsyncSession
) -> models.User:

    new_user = models.User(**user_data.model_dump())
    new_user.password = hash(user_data.password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
