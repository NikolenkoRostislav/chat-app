from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserCreate
from app.utils.security import get_password_hash

async def _get_user_by_field(db: AsyncSession, field_name: str, value) -> User | None:
    field = getattr(User, field_name)
    result = await db.execute(select(User).where(field == value))
    return result.scalar_one_or_none()

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
        return await _get_user_by_field(db, 'username', username)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        return await _get_user_by_field(db, 'email', email)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, id: str) -> User | None:
        return await _get_user_by_field(db, 'id', id)

    