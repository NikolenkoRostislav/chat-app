from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserReadPrivate, UserReadPublic, UserLogin
from app.utils.auth import get_current_user
from app.schemas.token import Token
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

@router.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    token = await UserService.login_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserReadPrivate)
async def read_self(user: User = Depends(get_current_user)):
    return user

@router.get("/{username}", response_model=UserReadPublic)
async def read_user(username: str, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
