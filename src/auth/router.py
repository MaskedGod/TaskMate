from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from ..database import get_session
from ..config import settings
from .models import User
from .utils import (
    create_access_token,
    create_user,
    verify_password,
    credentials_exception,
)
from .schemas import UserCreate, UserOut


auth_router = APIRouter(prefix="/users", tags=["Users"])


@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    new_user = await create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):

    # user = await session.select(User).filter(User.email == form_data.email).first()
    stmt = select(User).where(User.email == form_data.username)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password):
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
