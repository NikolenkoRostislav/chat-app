from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chat import ChatCreate, ChatRead
from app.services.chat import ChatService
from app.utils.auth import get_current_user
from app.models.chat import Chat
from app.models.user import User

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatRead)
async def create_chat(chat: ChatCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatService.create_chat(chat, db, current_user)
