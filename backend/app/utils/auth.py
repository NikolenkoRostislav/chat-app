from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends 
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.models import User
from app.utils.exceptions import *
from app.utils.security import verify_password
from app.db import DatabaseDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

def authenticate_user(user: User, password: str, db: AsyncSession) -> User:
    if not verify_password(password, user.password_hash):
        raise InvalidEntryError("Invalid password")
    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "refresh_token": create_refresh_token({"sub": str(user.id)})
    }

async def get_current_user(db: DatabaseDep, token: str = Depends(oauth2_scheme)) -> User:
    from app.services.user import UserService

    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise UnauthorizedError("Token missing user ID")
    except JWTError:
        raise UnauthorizedError("Invalid or expired token")
    user = await UserService.get_user_by_id(user_id, db) 
    if user is None:
        raise NotFoundError("User not found")
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]
