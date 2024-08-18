from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from ..models import Users

from ..database import get_session
from ..schemas import UserCreate, UserOut


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
):
    new_user = Users(**user_data.model_dump())

    session.add(new_user)

    await session.commit()
    await session.refresh(new_user)

    return new_user
