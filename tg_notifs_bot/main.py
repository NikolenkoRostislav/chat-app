import asyncio
import socketio
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import settings
from handlers import BotHandlers

sio = socketio.AsyncClient()
bot = Bot(token=settings.API_KEY)

@sio.on("notify")
async def send_notif(data):
    chat_name = data.get("chat_name")
    chat_ids = data.get("chat_ids", [])
    for cid in chat_ids:
        await bot.send_message(chat_id=cid, text=f"New message in {chat_name}!")

async def main():
    app = Application.builder().token(settings.API_KEY).build()
    BotHandlers.register_handlers(app)

    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    await sio.connect(
        settings.BACKEND_URL,
        socketio_path="ws/socket.io"
    )

    await sio.wait()

    await app.updater.stop()
    await app.stop()
    await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
