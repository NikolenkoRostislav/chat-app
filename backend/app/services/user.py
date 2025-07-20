from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserCreate
from app.utils.security import get_password_hash


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
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    