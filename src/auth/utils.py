from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from .models import User
from .schemas import UserCreate
from ..config import settings
from ..database import get_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")

credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(plain_password: str) -> str:

    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    try:
        new_user = User(**user_data.model_dump())
        if not new_user.email or not new_user.username or not new_user.password:
            raise ValueError("All fields must be provided and cannot be empty.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    new_user.password = hash_password(user_data.password)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def get_user(session: AsyncSession, username: EmailStr):
    stmt = select(User).filter(User.email == username)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User doesnt exist"
        )

    return user


async def authenticate_user(session: AsyncSession, username: EmailStr, password: str):
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
):

    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        username: str = payload.get("email")
        if username is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    user = await get_user(session, username)

    if user is None:
        raise credential_exception

    return user


async def login_user(user_credentials, session: AsyncSession):
    user = await authenticate_user(
        session, user_credentials.username, user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
