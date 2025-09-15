import aiohttp
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from config import settings

ASK_TEMP_CODE = range(1)

class BotHandlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to Chat App's notification bot!")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.BACKEND_URL}/tg-connection/status/{update.message.chat_id}") as resp:
                if await resp.json():
                    await update.message.reply_text("This Telegram account is already linked. If you want to link a different account, please disconnect from the web app first.")
                    return ConversationHandler.END
        await update.message.reply_text("Please enter a temporary code to link your account. You can generate this code from your account info page in the web app.")
        return ASK_TEMP_CODE

    @staticmethod
    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        return ConversationHandler.END

    @staticmethod
    async def handle_temp_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
        temp_code = update.message.text
        if not temp_code.isdigit() or not len(temp_code) == 6:
            await update.message.reply_text("Please send a valid code.")
            return ASK_TEMP_CODE
        await update.message.reply_text(f"Got your code: {temp_code}, verifying...")

        payload = {"temp_code": temp_code, "telegram_chat_id": update.message.chat_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.BACKEND_URL}/tg-connection/connect", params=payload) as resp:
                data = await resp.json()
                if resp.status != 200:
                    await update.message.reply_text("Failed to link your account. Please ensure the code is correct and try again.")
                    return ASK_TEMP_CODE    
                await update.message.reply_text("account successfully linked! You will start receiving notifications here.")

        return ConversationHandler.END  

    @staticmethod
    def register_handlers(app):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", BotHandlers.start)],
            states={
                ASK_TEMP_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, BotHandlers.handle_temp_code)],
            },
            fallbacks=[CommandHandler("cancel", BotHandlers.cancel)],
        )
        app.add_handler(conv_handler)
