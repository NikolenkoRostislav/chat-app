from asyncio import gather
import socketio
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.config import settings
from app.models import Chat, ChatMember, User
from app.services import UserService, ChatService
from app.utils.auth import decode_token
from app.db.database import SessionLocal
from app.db.session import get_db

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def identify_user(sid, data):
    rooms = list(sio.rooms(sid))
    for room in rooms:
        if room != sid:
            await sio.leave_room(sid, room)
    token = data.get("token")
    try:
        payload = decode_token(token)
        user_id = payload["sub"]
    except Exception:
        await sio.disconnect(sid)
        return

    async with SessionLocal() as db:
        user = await UserService.get_user_by_id(user_id, db)
        if user is None:
            await sio.disconnect(sid)
            return
        chats = await UserService.get_chats_by_current_user(db, user)
        for chat in chats:
            await sio.enter_room(sid, f"chat:{chat.id}")
            print(f"User {user.username} enetered chat with id {chat.id}")
    print(f"User {user.username} authenticated with sid {sid}")

async def _get_chat_info(chat_id: int):
    async with SessionLocal() as db:
        chat = await ChatService.get_chat_by_id(chat_id, db)
        chat_name = chat.name

        result = await db.execute(
            select(ChatMember)
            .options(
                selectinload(ChatMember.user).selectinload(User.telegram_connection)
            )
            .join(ChatMember.chat)
            .where(Chat.id == chat_id)
        )
        chat_members = result.scalars().all()
        tg_chat_ids = []
        for member in chat_members:
            if member.user.telegram_connection and member.user.telegram_connection.telegram_chat_id:
                tg_chat_ids.append(member.user.telegram_connection.telegram_chat_id)

        return tg_chat_ids, chat_name

@sio.event
async def new_message_sent(sid, data):
    chat_id = data.get("chat_id")
    await sio.emit("new_message_received", room=f"chat:{chat_id}")

    if settings.TELEGRAM_NOTIFICATIONS:
        tg_chat_ids, chat_name = await _get_chat_info(chat_id)
        notification_data = {
            "chat_ids": tg_chat_ids,
            "chat_name": chat_name
        }
        await sio.emit("notify", notification_data)
        print(f"Sending Telegram notification to members of chat with id {chat_id}")
