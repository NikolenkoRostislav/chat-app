from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db import get_db
from app.models import User
from app.utils.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth/login")

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def authenticate(db: AsyncSession, id: int, password: str) -> User | None: 
    from app.services.user import UserService

    user = await UserService.get_user_by_id(db, id) 
    if user and verify_password(password, user.password_hash): 
        return user 
    return None   

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    from app.services.user import UserService

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user = await UserService.get_user_by_id(db, user_id) 

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return user
