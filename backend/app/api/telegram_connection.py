from fastapi import APIRouter
from app.services import TelegramConnectionService
from app.utils.exceptions import handle_exceptions
from app.db import DatabaseDep

router = APIRouter(prefix="/tg-connection", tags=["tg_connection"])

@router.post("/connect")
@handle_exceptions
async def connect_user_to_bot(user_id: int, temp_code: str, telegram_chat_id: str, db: DatabaseDep):
    return await TelegramConnectionService.connect_user_to_bot(user_id, temp_code, telegram_chat_id, db)

@router.post("/temp-code")
@handle_exceptions
async def create_temp_code(user_id: int, db: DatabaseDep):
    return await TelegramConnectionService.create_temp_code(user_id, db)
