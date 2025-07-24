from sqlalchemy.ext.asyncio import AsyncSession
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