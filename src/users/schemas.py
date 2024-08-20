from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import mapped_column


class UserCreate(BaseModel):
    # id: int
    email: str
    username: str
    password: str
    # created_at: datetime  # = mapped_column(default=datetime.now(timezone.utc))
    # updated_at: datetime  # = mapped_column(default=datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
