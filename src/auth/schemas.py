from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: str
    username: str
    password: str

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
