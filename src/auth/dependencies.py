from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth.utils import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = verify_access_token(token)

    return payload
