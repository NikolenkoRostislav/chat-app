from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import MessageRead, MessageSend
from app.services import MessageService
from app.models import Message, User
from app.utils.auth import get_current_user
from app.utils.exceptions import handle_exceptions

router = APIRouter(prefix="/message", tags=["message"])

@router.post("/", response_model=MessageRead)
@handle_exceptions
async def send_message(message_data: MessageSend, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await MessageService.send_message(message_data, db, current_user)

@router.get("/chat/{chat_id}/user-messages/{user_id}", response_model=list[MessageRead])
@handle_exceptions
async def get_user_messages_in_chat(chat_id: int, user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await MessageService.get_user_messages_in_chat(chat_id, user_id, db, current_user)

@router.get("/chat-messages/{chat_id}", response_model=list[MessageRead])
@handle_exceptions
async def get_chat_messages(chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await MessageService.get_chat_messages(chat_id, db, current_user)

@router.get("/chat-messages/full-info/{chat_id}")
@handle_exceptions
async def get_chat_messages(chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await MessageService.get_chat_messages_full(chat_id, db, current_user)

@router.delete("/{message_id}")
@handle_exceptions
async def delete_message(message_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await MessageService.delete_message(message_id, db, current_user)