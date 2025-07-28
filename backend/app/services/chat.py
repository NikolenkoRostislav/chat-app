from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, User
from app.schemas import ChatCreate
from app.utils.exceptions import NotFoundError

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