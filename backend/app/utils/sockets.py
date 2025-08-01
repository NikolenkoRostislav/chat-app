import socketio
from app.schemas import MessageSend
from app.services import MessageService, UserService
from app.utils.auth import decode_access_token
from app.db.database import SessionLocal

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

connected_users = {}

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
async def send_message(sid, data):
    async with SessionLocal() as db:
        user = connected_users.get(sid)
        if user is None:
            await sio.disconnect(sid)
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
