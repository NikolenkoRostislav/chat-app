from fastapi import APIRouter
from app.schemas import MessageRead, MessageSend
from app.services import MessageService
from app.utils.exceptions import handle_exceptions
from app.db import DatabaseDep
from app.utils.auth import CurrentUserDep

router = APIRouter(prefix="/message", tags=["message"])

@router.post("/", response_model=MessageRead)
@handle_exceptions
async def send_message(message_data: MessageSend, db: DatabaseDep, current_user: CurrentUserDep):
    return await MessageService.send_message(message_data, db, current_user)

@router.get("/chat/{chat_id}")
@handle_exceptions
async def get_chat_messages(chat_id: int, db: DatabaseDep, current_user: CurrentUserDep):
    return await MessageService.get_chat_messages_full(chat_id, db, current_user)

@router.delete("/{message_id}")
@handle_exceptions
async def delete_message(message_id: int, db: DatabaseDep, current_user: CurrentUserDep):
    return await MessageService.delete_message(message_id, db, current_user)
