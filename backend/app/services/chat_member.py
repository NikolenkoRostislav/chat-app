from asyncio import gather
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
        result = await db.scalars(select(ChatMember).where(ChatMember.id == chat_member_id))
        chat_member = result.one_or_none()
        if strict and chat_member is None:
            raise NotFoundError("Chat member not found")
        return chat_member

    @staticmethod
    async def add_user_to_chat(chat_member_data: ChatMemberCreate, db: AsyncSession, current_user: User) -> ChatMember:
        chat, user, is_admin, is_member = await gather(
            ChatService.get_chat_by_id(chat_member_data.chat_id, db, True),
            UserService.get_user_by_id(chat_member_data.user_id, db, True),
            MembershipUtils.check_admin_status(current_user.id, chat_member_data.chat_id, db),
            MembershipUtils.check_user_membership(chat_member_data.user_id, chat_member_data.chat_id, db),
        )
        if not is_admin and chat.creator_id != current_user.id:
            raise PermissionDeniedError("You lack permission to add users to this chat")
        if is_member:
            raise AlreadyExistsError("User already in chat")
        chat_member = ChatMember(
            user_id=chat_member_data.user_id,
            chat_id=chat_member_data.chat_id
        )
        db.add(chat_member)
        await db.commit()
        return chat_member

    @staticmethod
    async def remove_member(chat_member_data: ChatMemberDelete, db: AsyncSession, current_user: User):
        user, chat, current_user_is_admin, user_to_delete_is_admin, chat_member = await gather(
            UserService.get_user_by_id(chat_member_data.user_id, db),
            ChatService.get_chat_by_id(chat_member_data.chat_id, db),
            MembershipUtils.check_admin_status(current_user.id, chat_member_data.chat_id, db),
            MembershipUtils.check_admin_status(chat_member_data.user_id, chat_member_data.chat_id, db),
            MembershipUtils.get_chat_member_by_user_and_chat_id(chat_member_data.user_id, chat_member_data.chat_id, db, True),
        )

        if current_user.id != user.id:
            if user_to_delete_is_admin and current_user.id != chat.creator_id:
                raise PermissionDeniedError("You cannot remove an admin from the chat unless you are the creator")
            if current_user.id != chat.creator_id and not current_user_is_admin:
                raise PermissionDeniedError("You lack permission to remove this user from the chat")
        if chat_member_data.user_id == chat.creator_id:
            raise PermissionDeniedError("Chat creator cannot be removed from the chat")

        await db.delete(chat_member)
        await db.commit()
        return {"detail": "User removed from chat"}

    @staticmethod
    async def update_chat_member_status(chat_member_id: int, is_admin: bool, db: AsyncSession, current_user: User) -> ChatMember:
        chat_member, chat = await gather(
            ChatMemberService.get_chat_member_by_id(chat_member_id, db, True),
            ChatService.get_chat_by_id(chat_member.chat_id, db, True),
        )
        if current_user.id != chat.creator_id:
            raise PermissionDeniedError("You lack permission to update this chat member's admin status")
        setattr(chat_member, "is_admin", is_admin)
        await db.commit()
        return chat_member