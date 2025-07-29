from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.models import User
from app.schemas import UserCreate
from app.utils.auth import create_access_token
from app.utils.exceptions import PermissionDeniedError, NotFoundError, AlreadyExistsError, InvalidEntryError
from app.utils.security import get_password_hash, verify_password

async def _get_user_by_field(field_name: str, value, db: AsyncSession, strict: bool) -> User | None:
    field = getattr(User, field_name)
    result = await db.execute(select(User).where(field == value))
    chat = result.scalar_one_or_none()
    if strict and chat is None:
        raise NotFoundError(f"User with {field_name} '{value}' not found")
    return chat

async def _update_field(user: User, field_name: str, value, db: AsyncSession) -> User | None:
    setattr(user, field_name, value)
    await db.commit()
    await db.refresh(user)
    return user

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
        existing_email = await UserService.get_user_by_email(user_data.email, db)
        existing_username = await UserService.get_user_by_username(user_data.username, db)
        if existing_email:
            raise AlreadyExistsError("Email already in use")
        elif existing_username:
            raise AlreadyExistsError("Username already in use")
        hashed = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed,
            pfp_url=user_data.pfp_url
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def login(username: str, password: str, db: AsyncSession) -> str:
        user = await UserService.get_user_by_username(username, db)
        if not user:
            raise InvalidEntryError("Invalid username")
        if not verify_password(password, user.password_hash):
            raise InvalidEntryError("Invalid password")
        return create_access_token({"sub": str(user.id)})

    @staticmethod
    async def get_user_by_username(username: str, db: AsyncSession, strict: bool = False) -> User | None:
        return await _get_user_by_field('username', username, db, strict)

    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession, strict: bool = False) -> User | None:
        return await _get_user_by_field('email', email, db, strict)

    @staticmethod
    async def get_user_by_id(id: str, db: AsyncSession, strict: bool = False) -> User | None:
        return await _get_user_by_field('id', id, db, strict)

    @staticmethod
    async def update_password(user: User, new_password: str, db: AsyncSession) -> User | None:
        return await _update_field(user, "password_hash", get_password_hash(new_password), db)
    
    @staticmethod
    async def update_username(user: User, new_username: str, db: AsyncSession) -> User | None:
        existing_username = await UserService.get_user_by_username(new_username, db)
        if existing_username is not None:
            raise AlreadyExistsError("Username already in use")
        return await _update_field(user, "username", new_username, db)

    @staticmethod
    async def update_email(user: User, new_email: str, db: AsyncSession) -> User | None:
        existing_email = await UserService.get_user_by_email(new_email, db)
        if existing_email is not None:
            raise AlreadyExistsError("Email already in use")
        return await _update_field(user, "email", new_email, db)

    @staticmethod
    async def update_pfp(user: User, new_pfp: str, db: AsyncSession) -> User | None:
        return await _update_field(user, "pfp_url", new_pfp, db)

    @staticmethod
    async def update_last_online(user: User, db: AsyncSession) -> User | None:
        return await _update_field(user, "last_online", datetime.utcnow(), db)
