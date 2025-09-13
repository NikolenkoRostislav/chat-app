from asyncio import gather
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.models import TelegramConnection, User
from app.utils.exceptions import *

class TelegramConnectionService:
    @staticmethod
    async def connect_user_to_bot(temp_code: str, db: AsyncSession, current_user: User):
        return "connected to bot (placeholder)"

    @staticmethod
    async def create_temp_code(db: AsyncSession, current_user: User):
        return "generated temp code (placeholder)"

