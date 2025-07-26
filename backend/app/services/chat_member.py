from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, User, ChatMember
from app.schemas import ChatMemberCreate
from app.services import ChatService, UserService
from app.utils.exceptions import PermissionDeniedError, NotFoundError

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
        chat = await ChatService.get_chat_by_id(db, chat_id)
        user = await UserService.get_user_by_id(db, user_id)
        if chat is None:
            raise NotFoundError("Chat not found")
        elif user is None:
            raise NotFoundError("User not found")
        result = await db.execute(select(ChatMember).where(ChatMember.user_id == user_id, ChatMember.chat_id == chat_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_chat_members_by_chat_id(chat_id: int, db: AsyncSession) -> list[ChatMember]:#I should probably remove this and write a method in ChatService
        result = await db.execute(select(ChatMember).where(ChatMember.chat_id == chat_id))
        return result.scalars().all()

    @staticmethod
    async def get_chat_members_by_user_id(user_id: int, db: AsyncSession) -> list[ChatMember]:#And replace this with a method in UserService
        result = await db.execute(select(ChatMember).where(ChatMember.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def remove_member(user_id: int, chat_id: int, db: AsyncSession, current_user: User):
        user = await UserService.get_user_by_id(db, user_id)
        chat = await ChatService.get_chat_by_id(db, chat_id)
        if current_user.id != chat.creator_id:
            raise PermissionDeniedError("You lack permission to remove this user from the chat")
        chat_member = await ChatMemberService.get_chat_member_by_user_and_chat_id(user_id, chat_id, db)
        if chat_member is None:
            raise NotFoundError("User is not a member of this chat")
        await db.delete(chat_member)
        await db.commit()
        return {"detail": "User removed from chat"}