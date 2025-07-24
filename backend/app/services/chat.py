from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Chat, User
from app.schemas import ChatCreate

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
    async def get_chat_by_id(db: AsyncSession, chat_id: int) -> Chat | None:
        result = await db.execute(select(Chat).where(Chat.id == chat_id))
        return result.scalar_one_or_none()