import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import mapped_column


class UserCreate(BaseModel):
    # id: int
    email: str
    username: str
    password: str
    # created_at: datetime.datetime = mapped_column(
    #     default=datetime.datetime.now(datetime.timezone.utc)
    # )
    # updated_at: datetime.datetime = mapped_column(
    #     default=datetime.datetime.now(datetime.timezone.utc)
    # )

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    pass


class UserOut(BaseModel):
    email: EmailStr
    username: str
    # created_at: datetime.datetime

    class Config:
        arbitrary_types_allowed = True
