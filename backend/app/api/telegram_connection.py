from fastapi import APIRouter
from app.services import TelegramConnectionService
from app.utils.exceptions import handle_exceptions
from app.db import DatabaseDep
from app.utils.auth import CurrentUserDep

router = APIRouter(prefix="/tg-connection", tags=["tg_connection"])

@router.post("/connect")
@handle_exceptions
async def connect_user_to_bot(temp_code: str, db: DatabaseDep, current_user: CurrentUserDep):
    return await TelegramConnectionService.connect_user_to_bot(temp_code, db, current_user)

@router.post("/temp-code")
@handle_exceptions
async def create_temp_code(db: DatabaseDep, current_user: CurrentUserDep):
    return await TelegramConnectionService.create_temp_code(db, current_user)
