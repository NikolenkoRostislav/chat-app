import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from app.models import TelegramConnection
from app.services import UserService
from app.utils.exceptions import *

async def _update_field(connection: TelegramConnection, field_name: str, value, db: AsyncSession) -> TelegramConnection | None:
    setattr(connection, field_name, value)
    await db.commit()
    return connection

class TelegramConnectionService:
    @staticmethod
    async def create_new_connection(user_id: int, db: AsyncSession) -> TelegramConnection:
        await UserService.get_user_by_id(user_id, db, True)
        new_connection = TelegramConnection(user_id=user_id, code_expiry_time=datetime.utcnow())
        db.add(new_connection)
        await db.commit()
        return new_connection

    @staticmethod
    async def get_connection_by_user_id(user_id: int, db: AsyncSession, auto_create: bool = False) -> TelegramConnection | None:
        await UserService.get_user_by_id(user_id, db, True)
        result = await db.scalars(select(TelegramConnection).where(TelegramConnection.user_id == user_id))
        connection = result.one_or_none()
        if auto_create and connection is None:
            return await TelegramConnectionService.create_new_connection(user_id, db)
        return connection

    @staticmethod
    async def get_connection_by_temp_code(temp_code: str, db: AsyncSession, strict: bool = False) -> TelegramConnection | None:
        if temp_code is None: raise InvalidEntryError("Temporary code is required")
        result = await db.scalars(select(TelegramConnection).where(
            TelegramConnection.temp_code == temp_code, TelegramConnection.code_expiry_time > datetime.utcnow()
        ))
        connection = result.one_or_none()
        if connection is None and strict: raise NotFoundError("Invalid or expired temporary code")
        return connection

    @staticmethod
    async def get_connection_by_chat_id(telegram_chat_id: str, db: AsyncSession, strict: bool = False) -> TelegramConnection | None:
        if telegram_chat_id is None: raise InvalidEntryError("Telegram chat ID is required")
        result = await db.scalars(select(TelegramConnection).where(
            TelegramConnection.telegram_chat_id == telegram_chat_id
        ))
        connection = result.one_or_none()
        if connection is None and strict: raise NotFoundError("No connection found for the provided Telegram chat ID")
        return connection

    @staticmethod
    async def connect_user(temp_code: str, telegram_chat_id: str, db: AsyncSession):
        connection = await TelegramConnectionService.get_connection_by_temp_code(temp_code, db, True)
        await _update_field(connection, 'telegram_chat_id', telegram_chat_id, db)
        return connection

    @staticmethod
    async def disconnect_user(user_id: int, db: AsyncSession):
        connection = await TelegramConnectionService.get_connection_by_user_id(user_id, db, True)
        await _update_field(connection, 'telegram_chat_id', "Disconnected", db)
        return {"detail": "User disconnected successfully"}

    @staticmethod
    async def create_temp_code(user_id: int, db: AsyncSession):
        connection = await TelegramConnectionService.get_connection_by_user_id(user_id, db, True)
        code = str(secrets.randbelow(10**6)).zfill(6)
        code_expiry_time = datetime.utcnow() + timedelta(minutes=10)
        if await TelegramConnectionService.get_connection_by_temp_code(code, db):
            return await TelegramConnectionService.create_temp_code(user_id, db)
        await _update_field(connection, 'temp_code', code, db)
        await _update_field(connection, 'code_expiry_time', code_expiry_time, db)
        return {"code": code}
