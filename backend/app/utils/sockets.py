import socketio
from app.schemas import MessageSend, ChatMemberCreate
from app.services import MessageService, UserService, ChatMemberService
from app.utils.auth import decode_token
from app.db.database import SessionLocal

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

@sio.event
async def new_message_sent(sid, data):
    chat_id = data.get("chat_id")
    await sio.emit("new_message_received", room=f"chat:{chat_id}")
