from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

ASK_TEMP_CODE = range(1)

class BotHandlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to Chat App's notification bot!")
        await update.message.reply_text("Please enter a temporary code to link your account. You can generate this code from your account info page in the web app.")
        return ASK_TEMP_CODE

    @staticmethod
    async def handle_temp_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        if not user_input.isdigit() or not len(user_input) == 6:
            await update.message.reply_text("Please send a valid code.")
            return ASK_TEMP_CODE
        number = int(user_input)
        await update.message.reply_text(f"Got your code: {number}, verifying...")

        # call API to verify code and link account, I'll add this later

        return ConversationHandler.END  

    @staticmethod
    def register_handlers(app):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", BotHandlers.start)],
            states={
                ASK_TEMP_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, BotHandlers.handle_temp_code)],
            },
            fallbacks=[],
        )
        app.add_handler(conv_handler)
