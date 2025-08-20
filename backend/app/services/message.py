from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, Message
from app.schemas import MessageSend, UserReadPublic
from app.utils.exceptions import PermissionDeniedError, NotFoundError, AlreadyExistsError, InvalidEntryError
from app.utils.membership import MembershipUtils

class MessageService:
    @staticmethod
    async def send_message(message_data: MessageSend, db: AsyncSession, current_user: User) -> Message:
        if not await MembershipUtils.check_user_membership(current_user.id, message_data.chat_id, db):
            raise PermissionDeniedError("You are not a member of this chat")
        message = Message(
            chat_id = message_data.chat_id,
            sender_id = current_user.id,
            content = message_data.content,
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message
    
    @staticmethod
    async def get_message_by_id(message_id: int, db: AsyncSession, strict: bool = False) -> Message | None:
        result = await db.execute(select(Message).where(Message.id == message_id))
        message = result.scalar_one_or_none()
        if strict and message is None:
            raise NotFoundError("Message not found")
        return message

    @staticmethod
    async def delete_message(message_id: int, db: AsyncSession, current_user: User):
        message = await MessageService.get_message_by_id(message_id, db, strict=True)
        chat = message.chat
        if message.sender_id != current_user.id and chat.creator_id != current_user.id:
            raise PermissionDeniedError("You lack permission to delete this message")
        await db.delete(message)
        await db.commit()
        return {"detail": "Message deleted successfully"}

    @staticmethod
    async def get_user_messages_in_chat(chat_id: int, user_id: int, db: AsyncSession, current_user: User) -> list[Message]:
        if not await MembershipUtils.check_user_membership(current_user.id, chat_id, db):
            raise PermissionDeniedError("You are not a member of this chat")
        result = await db.execute(select(Message).where(Message.chat_id == chat_id, Message.sender_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def get_chat_messages(chat_id: int, db: AsyncSession, current_user: User) -> list[Message]:
        if not await MembershipUtils.check_user_membership(current_user.id, chat_id, db):
            raise PermissionDeniedError("You are not a member of this chat")
        result = await db.execute(select(Message).where(Message.chat_id == chat_id))
        return result.scalars().all()

    @staticmethod
    async def get_chat_messages_full(chat_id: int, db: AsyncSession, current_user: User):
        chat_messages = await MessageService.get_chat_messages(chat_id, db, current_user)
        full_messages = []
        for message in chat_messages:
            full_messages.append({
                "sender_id": message.sender_id,
                "content": message.content,
                "sent_at": message.timestamp,
                "user": UserReadPublic.from_orm(message.sender)
            })
        return full_messages
