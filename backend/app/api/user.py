from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import UserCreate, UserUpdateEmail, UserUpdatePassword, UserUpdateUsername, UserUpdatePFP, UserReadPrivate, UserReadPublic, UserLogin, Token
from app.services import UserService
from app.utils.auth import get_current_user
from app.utils.exceptions import handle_exceptions
from app.models import User

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register", response_model=UserReadPublic)
@handle_exceptions
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.create_user(user, db)

@router.post("/auth/login", response_model=Token)
@handle_exceptions
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    token = await UserService.login(form_data.username, form_data.password, db)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserReadPrivate)
@handle_exceptions
async def read_self(user: User = Depends(get_current_user)):
    return user

@router.get("/id/{user_id}", response_model=UserReadPublic)
@handle_exceptions
async def read_user(user_id: str, db: AsyncSession = Depends(get_db)):
    return await UserService.get_user_by_id(int(user_id), db, True)

@router.get("/{username}", response_model=UserReadPublic)
@handle_exceptions
async def read_user(username: str, db: AsyncSession = Depends(get_db)):
    return await UserService.get_user_by_username(username, db, True)

@router.patch("/update/pfp", response_model=UserReadPublic)
@handle_exceptions
async def update_pfp(new_pfp: UserUpdatePFP, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_pfp(user, new_pfp.pfp_url, db)

@router.patch("/update/password", response_model=UserReadPublic)
@handle_exceptions
async def update_password(new_password: UserUpdatePassword, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_password(user, new_password.password, db)

@router.patch("/update/username", response_model=UserReadPublic)
@handle_exceptions
async def update_username(new_username: UserUpdateUsername, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_username(user, new_username.username, db)

@router.patch("/update/email", response_model=UserReadPublic)
@handle_exceptions
async def update_email(new_email: UserUpdateEmail, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_email(user, new_email.email, db)

@router.patch("/update/last-online", response_model=UserReadPublic)
@handle_exceptions
async def update_last_online(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update_last_online(user, db)
