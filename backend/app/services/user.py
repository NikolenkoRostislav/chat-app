from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserCreate
from app.utils.auth import create_access_token
from app.utils.exceptions import PermissionDeniedError, NotFoundError, AlreadyExistsError, InvalidEntryError
from app.utils.security import get_password_hash, verify_password

async def _get_user_by_field(db: AsyncSession, field_name: str, value, strict: bool) -> User | None:
    field = getattr(User, field_name)
    result = await db.execute(select(User).where(field == value))
    chat = result.scalar_one_or_none()
    if strict and chat is None:
        raise NotFoundError(f"User with {field_name} '{value}' not found")
    return chat

async def _update_field(db: AsyncSession, user: User, field_name: str, value) -> User | None:
    setattr(user, field_name, value)
    await db.commit()
    await db.refresh(user)
    return user

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        existing_email = await UserService.get_user_by_email(db, user_data.email)
        existing_username = await UserService.get_user_by_username(db, user_data.username)
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
    async def login(db: AsyncSession, username: str, password: str) -> str:
        user = await UserService.get_user_by_username(db, username)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidEntryError("Invalid credentials")
        return create_access_token({"sub": str(user.id)})

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str, strict: bool = False) -> User | None:
        return await _get_user_by_field(db, 'username', username, strict)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str, strict: bool = False) -> User | None:
        return await _get_user_by_field(db, 'email', email, strict)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: str, strict: bool = False) -> User | None:
        return await _get_user_by_field(db, 'id', id, strict)

    @staticmethod
    async def update_password(db: AsyncSession, user: User, new_password: str) -> User | None:
        return await _update_field(db, user, "password", new_password)
    
    @staticmethod
    async def update_username(db: AsyncSession, user: User, new_username: str) -> User | None:
        existing_username = await UserService.get_user_by_username(db, new_username)
        if existing_username is not None:
            raise AlreadyExistsError("Username already in use")
        return await _update_field(db, user, "username", new_username)

    @staticmethod
    async def update_email(db: AsyncSession, user: User, new_email: str) -> User | None:
        existing_email = await UserService.get_user_by_email(db, new_email)
        if existing_email is not None:
            raise AlreadyExistsError("Email already in use")
        return await _update_field(db, user, "email", new_email)

    @staticmethod
    async def update_pfp(db: AsyncSession, user: User, new_pfp: str) -> User | None:
        return await _update_field(db, user, "pfp_url", new_pfp)


    