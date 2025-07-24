from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserCreate
from app.utils.auth import create_access_token
from app.utils.security import get_password_hash, verify_password

async def _get_user_by_field(db: AsyncSession, field_name: str, value) -> User | None:
    field = getattr(User, field_name)
    result = await db.execute(select(User).where(field == value))
    return result.scalar_one_or_none()

async def _update_user_field(db: AsyncSession, user: User, field_name: str, value) -> User | None:
    setattr(user, field_name, value)
    await db.commit()
    await db.refresh(user)
    return user

class UserService:
    @staticmethod
    async def create_user(db: AsyncSession, user: UserCreate) -> User:
        hashed = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            password_hash=hashed,
            pfp_url=user.pfp_url
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def login_user(db: AsyncSession, username: str, password: str) -> str:
        user = await UserService.get_user_by_username(db, username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return create_access_token({"sub": str(user.id)})

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        return await _get_user_by_field(db, 'username', username)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        return await _get_user_by_field(db, 'email', email)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: str) -> User | None:
        return await _get_user_by_field(db, 'id', id)

    @staticmethod
    async def update_user_password(db: AsyncSession, user: User, new_password: str) -> User | None:
        return await _update_user_field(db, user, "password", new_password)
    
    @staticmethod
    async def update_user_username(db: AsyncSession, user: User, new_username: str) -> User | None:
        return await _update_user_field(db, user, "username", new_username)

    @staticmethod
    async def update_user_email(db: AsyncSession, user: User, new_email: str) -> User | None:
        return await _update_user_field(db, user, "email", new_email)

    @staticmethod
    async def update_user_pfp(db: AsyncSession, user: User, new_pfp: str) -> User | None:
        return await _update_user_field(db, user, "pfp_url", new_pfp)


    