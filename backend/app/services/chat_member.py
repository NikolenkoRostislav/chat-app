from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, User, ChatMember
from app.schemas import ChatMemberCreate, ChatMemberDelete
from app.services import ChatService, UserService
from app.utils.exceptions import *
from app.utils.membership import MembershipUtils

class ChatMemberService:
    @staticmethod
    async def get_chat_member_by_id(chat_member_id: int, db: AsyncSession, strict: bool = False) -> ChatMember | None:
        result = await db.execute(select(ChatMember).where(ChatMember.id == chat_member_id))
        chat_member = result.scalar_one_or_none()
        if strict and chat_member is None:
            raise NotFoundError("Chat member not found")
        return chat_member

    @staticmethod
    async def add_user_to_chat(chat_member_data: ChatMemberCreate, db: AsyncSession, current_user: User) -> ChatMember:
        chat = await ChatService.get_chat_by_id(chat_member_data.chat_id, db, True)
        user = await UserService.get_user_by_id(chat_member_data.user_id, db, True)
        if not await MembershipUtils.check_admin_status(current_user.id, chat_member_data.chat_id, db) and chat.creator_id != current_user.id:
            raise PermissionDeniedError("You lack permission to add users to this chat")
        if await MembershipUtils.check_user_membership(chat_member_data.user_id, chat_member_data.chat_id, db):
            raise AlreadyExistsError("User already in chat")
        chat_member = ChatMember(
            user_id=chat_member_data.user_id,
            chat_id=chat_member_data.chat_id
        )
        db.add(chat_member)
        await db.commit()
        await db.refresh(chat_member)
        return chat_member

    @staticmethod
    async def remove_member(chat_member_data: ChatMemberDelete, db: AsyncSession, current_user: User):
        user = await UserService.get_user_by_id(chat_member_data.user_id, db)
        chat = await ChatService.get_chat_by_id(chat_member_data.chat_id, db)
        if current_user.id != user.id:
            current_user_is_admin = await MembershipUtils.check_admin_status(current_user.id, chat_member_data.chat_id, db)
            user_to_delete_is_admin = await MembershipUtils.check_admin_status(chat_member_data.user_id, chat_member_data.chat_id, db)
            if user_to_delete_is_admin and current_user.id != chat.creator_id:
                raise PermissionDeniedError("You cannot remove an admin from the chat unless you are the creator")
            if current_user.id != chat.creator_id and not current_user_is_admin:
                raise PermissionDeniedError("You lack permission to remove this user from the chat")
        if chat_member_data.user_id == chat.creator_id:
            raise PermissionDeniedError("Chat creator cannot be removed from the chat")
        if not await MembershipUtils.check_user_membership(chat_member_data.user_id, chat_member_data.chat_id, db):
            raise InvalidEntryError("User is not a member of this chat")
        chat_member = await MembershipUtils.get_chat_member_by_user_and_chat_id(chat_member_data.user_id, chat_member_data.chat_id, db, True)
        await db.delete(chat_member)
        await db.commit()
        return {"detail": "User removed from chat"}

    @staticmethod
    async def update_chat_member_status(chat_member_id: int, is_admin: bool, db: AsyncSession, current_user: User) -> ChatMember:
        chat_member = await ChatMemberService.get_chat_member_by_id(chat_member_id, db, True)
        chat = await ChatService.get_chat_by_id(chat_member.chat_id, db, True)
        if current_user.id != chat.creator_id:
            raise PermissionDeniedError("You lack permission to update this chat member's admin status")
        setattr(chat_member, "is_admin", is_admin)
        db.add(chat_member)
        await db.commit()
        await db.refresh(chat_member)
        return chat_member