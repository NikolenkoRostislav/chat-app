from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import UserCreate, UserUpdateEmail, UserReadPrivate, UserReadPublic, UserLogin, Token
from app.services import UserService
from app.utils.auth import get_current_user
from app.utils.exceptions import handle_exceptions
from app.models import User

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register", response_model=UserReadPublic)
@handle_exceptions
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(db, user)

@router.post("/auth/login", response_model=Token)
@handle_exceptions
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    token = await UserService.login(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserReadPrivate)
@handle_exceptions
async def read_self(user: User = Depends(get_current_user)):
    return user

@router.get("/{username}", response_model=UserReadPublic)
@handle_exceptions
async def read_user(username: str, db: AsyncSession = Depends(get_db)):
    return await UserService.get_user_by_username(db, username, True)

@router.patch("/update/pfp", response_model=UserReadPublic)
@handle_exceptions
async def update_pfp(new_pfp: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_pfp(db, user, new_pfp)

@router.patch("/update/password", response_model=UserReadPublic)
@handle_exceptions
async def update_password(new_password: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_password(db, user, new_password)

@router.patch("/update/username", response_model=UserReadPublic)
@handle_exceptions
async def update_username(new_username: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_username(db, user, new_username)

@router.patch("/update/email", response_model=UserReadPublic)
@handle_exceptions
async def update_email(new_email: UserUpdateEmail, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_email(db, user, new_email.email)
