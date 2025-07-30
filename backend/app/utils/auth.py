from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db import get_db
from app.utils.exceptions import InvalidEntryError
from app.models import User
from app.utils.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth/login")

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def authenticate_user(user: User, password: str, db: AsyncSession) -> User:
    if not verify_password(password, user.password_hash):
        raise InvalidEntryError("Invalid password")
    return create_access_token({"sub": str(user.id)})

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    from app.services.user import UserService

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token missing user ID")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await UserService.get_user_by_id(user_id, db) 
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
