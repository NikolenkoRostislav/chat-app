from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

class BotHandlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to Chat App's notification bot!")

    @staticmethod
    async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Test successful!")

    @staticmethod
    def register_handlers(app):
        app.add_handler(CommandHandler("start", BotHandlers.start))
        app.add_handler(CommandHandler("test", BotHandlers.test))