from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.users.models import Users
from src.users.schemas import UserCreate, UserOut, UserUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


class UserFactory:

    async def create_user(user_data: UserCreate, session: AsyncSession) -> Users:

        new_user = Users(**user_data.model_dump())
        new_user.password = hash(user_data.password)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
