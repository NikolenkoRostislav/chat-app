from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, User, ChatMember
from app.schemas import ChatCreate
from app.utils.exceptions import *
from app.utils.membership import MembershipUtils

class ChatService:
    @staticmethod
    async def create_chat(chat_data: ChatCreate, db: AsyncSession, current_user: User) -> Chat:
        chat = Chat(
            name=chat_data.name,
            icon_url=chat_data.icon_url,
            creator_id=current_user.id
        )
        db.add(chat)
        await db.commit()
        await db.refresh(chat)
        return chat

    @staticmethod   
    async def get_chat_by_id(chat_id: int, db: AsyncSession, strict: bool = False) -> Chat | None:
        result = await db.execute(select(Chat).where(Chat.id == chat_id))
        chat = result.scalar_one_or_none()
        if strict and chat is None:
            raise NotFoundError("Chat not found")
        return chat

    @staticmethod
    async def get_chat_members_by_chat_id(chat_id: int, db: AsyncSession, current_user: User) -> list[ChatMember]:
        chat = await ChatService.get_chat_by_id(chat_id, db, True)
        if not await MembershipUtils.check_user_membership(current_user.id, chat_id, db) and chat.creator_id != current_user.id:
            raise PermissionDeniedError("You lack permission to view this chat's members")
        await db.refresh(chat)
        return chat.members

    @staticmethod
    async def get_chat_member_count(chat_id: int, db: AsyncSession, current_user: User) -> int:
        chat_members = await ChatService.get_chat_members_by_chat_id(chat_id, db, current_user)
        return len(chat_members)