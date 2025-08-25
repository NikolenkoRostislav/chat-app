from fastapi import APIRouter
from app.schemas import UserCreate, UserUpdateEmail, UserUpdatePassword, UserUpdateUsername, UserUpdatePFP, UserReadPrivate, UserReadPublic, UserLogin, Token, ChatRead
from app.services import UserService
from app.utils.exceptions import handle_exceptions
from app.db import DatabaseDep
from app.utils.auth import CurrentUserDep

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register", response_model=UserReadPublic)
@handle_exceptions
async def register(user: UserCreate, db: DatabaseDep):
    return await UserService.create_user(user, db)

@router.get("/me", response_model=UserReadPrivate)
@handle_exceptions
async def read_self(current_user: CurrentUserDep):
    return current_user

@router.get("/chats/me", response_model=list[ChatRead])
@handle_exceptions
async def get_chats_me(db: DatabaseDep, current_user: CurrentUserDep):
    return await UserService.get_chats_by_current_user(db, current_user)

@router.get("/{username}", response_model=UserReadPublic)
@handle_exceptions
async def read_user(username: str, db: DatabaseDep):
    return await UserService.get_user_by_username(username, db, True)

@router.get("/id/{user_id}", response_model=UserReadPublic)
@handle_exceptions
async def read_user(user_id: str, db: DatabaseDep):
    return await UserService.get_user_by_id(int(user_id), db, True)

@router.patch("/update/pfp", response_model=UserReadPublic)
@handle_exceptions
async def update_pfp(new_pfp: UserUpdatePFP, current_user: CurrentUserDep, db: DatabaseDep):
    return await UserService.update_pfp(current_user, new_pfp.pfp_url, db)

@router.patch("/update/username", response_model=UserReadPublic)
@handle_exceptions
async def update_username(new_username: UserUpdateUsername, current_user: CurrentUserDep, db: DatabaseDep):
    return await UserService.update_username(current_user, new_username.username, db)

@router.patch("/update/email", response_model=UserReadPublic)
@handle_exceptions
async def update_email(new_email: UserUpdateEmail, current_user: CurrentUserDep, db: DatabaseDep):
    return await UserService.update_email(current_user, new_email.email, db)

@router.patch("/update/last-online", response_model=UserReadPublic)
@handle_exceptions
async def update_last_online(current_user: CurrentUserDep, db: DatabaseDep):
    return await UserService.update_last_online(current_user, db)
