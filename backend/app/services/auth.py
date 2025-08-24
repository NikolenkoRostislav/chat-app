from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from app.services import UserService
from app.utils.auth import create_access_token, create_refresh_token, decode_token, authenticate_user
from app.utils.security import get_password_hash, verify_password
from app.utils.exceptions import *

class AuthService:
    @staticmethod
    async def login(username: str, password: str, db: AsyncSession) -> dict:
        user = await UserService.get_user_by_username(username, db)
        if not user:
            raise InvalidEntryError("Invalid username")
        tokens = authenticate_user(user, password, db)
        return {**tokens, "token_type": "bearer"}

    @staticmethod
    async def refresh(refresh_token: str, db: AsyncSession) -> dict:
        try:
            payload = decode_token(refresh_token)
            user_id = int(payload.get("sub"))
        except JWTError:
            raise UnauthorizedError("Invalid or expired refresh token")
        
        access_token = create_access_token({"sub": str(user_id)})
        new_refresh_token = create_refresh_token({"sub": str(user_id)})
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
