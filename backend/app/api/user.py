from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserReadPrivate, UserReadPublic
from app.services.user import UserService
from app.models.user import User


router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register", response_model=UserReadPublic)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_email = await UserService.get_user_by_email(db, user.email)
    existing_username = await UserService.get_user_by_username(db, user.username)
    if existing_email or existing_username:
        raise HTTPException(status_code=400, detail="Email or Username already in use")

    return await UserService.create_user(db, user)
