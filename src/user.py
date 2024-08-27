from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status

from . import service
from .database import get_session
from .schemas import UserCreate, UserOut


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    new_user = await service.create_user(user_data, session)

    return new_user
