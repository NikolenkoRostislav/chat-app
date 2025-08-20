from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import ChatMember
from app.services import ChatService, UserService
from app.utils.exceptions import PermissionDeniedError, NotFoundError, AlreadyExistsError, InvalidEntryError

class MembershipUtils:
    @staticmethod
    async def get_chat_member_by_user_and_chat_id(user_id: int, chat_id: int, db: AsyncSession, strict: bool = False) -> ChatMember | None:
        chat = await ChatService.get_chat_by_id(chat_id, db, True)
        user = await UserService.get_user_by_id(user_id, db, True)
        result = await db.execute(select(ChatMember).where(ChatMember.user_id == user_id, ChatMember.chat_id == chat_id))
        chat_member = result.scalar_one_or_none()
        if strict and chat_member is None:
            raise NotFoundError("Chat member not found")
        return chat_member

    @staticmethod
    async def check_user_membership(user_id: int, chat_id: int, db: AsyncSession) -> bool:
        chat_member = await MembershipUtils.get_chat_member_by_user_and_chat_id(user_id, chat_id, db)
        return chat_member is not None

    @staticmethod
    async def check_admin_status(user_id: int, chat_id: int, db: AsyncSession) -> bool:
        chat_member = await MembershipUtils.get_chat_member_by_user_and_chat_id(user_id, chat_id, db)
        if chat_member is None:
            return False
        return chat_member.is_admin