from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from src.users.utils import UserFactory
from ..database import get_session
from .schemas import UserCreate, UserOut


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    new_user = await UserFactory.create_user(user_data, session)

    return new_user
