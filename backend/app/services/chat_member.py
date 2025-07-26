from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, User, ChatMember
from app.schemas import ChatMemberCreate

class ChatMemberService:
    @staticmethod
    async def add_user_to_chat(user_id: int, chat_id: int, db: AsyncSession) -> ChatMember:
        chat_member = ChatMember(
            user_id=user_id,
            chat_id=chat_id
        )
        db.add(chat_member)
        await db.commit()
        await db.refresh(chat_member)
        return chat_member

    @staticmethod
    async def get_chat_member_by_id(chat_member_id: int, db: AsyncSession) -> ChatMember | None:
        result = await db.execute(select(ChatMember).where(ChatMember.id == chat_member_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_chat_member_by_user_and_chat_id(user_id: int, chat_id: int, db: AsyncSession) -> ChatMember | None:
        result = await db.execute(select(ChatMember).where(ChatMember.user_id == user_id, ChatMember.chat_id == chat_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_chat_members_by_chat_id(chat_id: int, db: AsyncSession) -> list[ChatMember]:
        result = await db.execute(select(ChatMember).where(ChatMember.chat_id == chat_id))
        return result.scalars().all()

    @staticmethod
    async def get_chat_members_by_user_id(user_id: int, db: AsyncSession) -> list[ChatMember]:
        result = await db.execute(select(ChatMember).where(ChatMember.user_id == user_id))
        return result.scalars().all()