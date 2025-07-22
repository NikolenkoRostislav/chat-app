from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings

from app.utils.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth/login")

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def authenticate(db: AsyncSession, email: str, password: str) -> User | None: 
    from app.services.user import UserService
    
    user = await UserService.get_user_by_email(db, email) 
    if user and verify_password(password, user.password_hash): 
        return user 
    return None   