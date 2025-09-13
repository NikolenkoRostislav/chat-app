from asyncio import gather
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from app.models import TelegramConnection
from app.utils.exceptions import *

class TelegramConnectionService:
    @staticmethod
    async def create_new_connection(user_id: int, db: AsyncSession) -> TelegramConnection:
        new_connection = TelegramConnection(user_id=user_id, code_expiry_time=datetime.utcnow())
        db.add(new_connection)
        await db.commit()
        return new_connection

    @staticmethod
    async def get_connection_by_user_id(user_id: int, db: AsyncSession, auto_create: bool = False) -> TelegramConnection | None:
        connection = await db.scalars(select(TelegramConnection).where(TelegramConnection.user_id == user_id))
        result = connection.one_or_none()
        if auto_create and result is None:
            return await TelegramConnectionService.create_new_connection(user_id, db)
        return result

    @staticmethod
    async def connect_user_to_bot(user_id: int, temp_code: str, telegram_chat_id: str, db: AsyncSession):
        connection = await TelegramConnectionService.get_connection_by_user_id(user_id, db, True)
        if connection.temp_code != temp_code or connection.code_expiry_time < datetime.utcnow():
            raise InvalidEntryError("Invalid or expired temporary code")
        #Update connection details to include telegram_chat_id
        return "connected to bot (placeholder)"

    @staticmethod
    async def create_temp_code(user_id: int, db: AsyncSession):
        connection = await TelegramConnectionService.get_connection_by_user_id(user_id, db, True)
        code = str(secrets.randbelow(10**6)).zfill(6)
        code_expiry_time = datetime.utcnow() + timedelta(minutes=10)
        #Update connection with new temp code and expiry time
        return {"generated temp code (placeholder)": code, "expires_at (placeholder)": code_expiry_time}
