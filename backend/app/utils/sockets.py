"""
import socketio
from app.schemas import MessageSend, ChatMemberCreate
from app.services import MessageService, UserService, ChatMemberService
from app.utils.auth import decode_access_token
from app.db.database import SessionLocal

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

connected_users = {}

async def _get_user_by_sid(sid):
    user = connected_users.get(sid)
    if user is None:
        await sio.disconnect(sid)
        return
    return user

@sio.event
async def identify_user(sid, data):
    token = data.get("token")
    try:
        payload = decode_access_token(token)
        user_id = payload["sub"]
    except Exception:
        await sio.disconnect(sid)
        return

    async with SessionLocal() as db:
        user = UserService.get_user_by_id(user_id, db)
        if user is None:
            await sio.disconnect(sid)
        return
    connected_users[sid] = user
    await sio.enter_room(sid, f"user:{user.id}")
    print(f"User {user.username} authenticated with sid {sid}")

@sio.event 
async def connect_user_to_chat(sid, data):
    user = await _get_user_by_sid(sid)
    if user is None:
        return
    chat_id = data.get("chat_id")
    if chat_id is None:
        await sio.emit("error", {"error": "Chat ID is required"}, room=sid)
        return
    await sio.enter_room(sid, f"chat:{chat_id}")
    print(f"User {user.username} with sid {sid} connected to chat with id {chat_id}")

@sio.event
async def send_message(sid, data):
    async with SessionLocal() as db:
        user = await _get_user_by_sid(sid)
        if user is None:
            return
        try:
            message_data = MessageSend(**data)
            message = await MessageService.send_message(message_data, db, user)
        except Exception as e:
            await sio.emit("error", {"error": str(e)}, room=sid)
            return
        await sio.emit(
            "new_message",
            {
                "chat_id": message.chat_id,
                "sender_id": message.sender_id,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
            },
            room=f"chat:{message.chat_id}"
        )

@sio.event 
async def add_user_to_chat(sid, data):
    async with SessionLocal() as db:
        user = await _get_user_by_sid(sid)
        if user is None:
            return
        try:
            chat_member_data = ChatMemberCreate(**data)
            chat_member = await ChatMemberService.add_user_to_chat(chat_member_data, db, user)
        except Exception as e:
            await sio.emit("error", {"error": str(e)}, room=sid)
            return
        await sio.emit(
            "new_chat_member",
            {
                "chat_id": chat_member.chat_id,
                "user_id": chat_member.user_id,
                "is_admin": chat_member.is_admin,
            },
            room=f"chat:{chat_member.chat_id}"
        )

@sio.event
async def disconnect(sid):
    user = connected_users.pop(sid, None)
    if user:
        print(f"User {user.username} disconnected")
"""
# I'll use sockets in frontend in the next version