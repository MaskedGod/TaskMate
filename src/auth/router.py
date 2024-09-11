from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from ..database import get_session
from .utils import (
    create_user,
    get_current_user,
    login_user,
)
from .schemas import UserCreate, UserOut


auth_router = APIRouter(prefix="/user", tags=["User"])


@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    new_user = await create_user(user_data, session)

    return new_user


@auth_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def user_authentication(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):

    access_token = await login_user(user_credentials, session)

    return access_token


@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_authenticated_user(
    current_user=Depends(get_current_user),
):
    return current_user
