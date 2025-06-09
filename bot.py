import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.start import start
from handlers.message import handle_message
from handlers.callback import button_callback
from handlers.admin import admin, handle_admin_callback, handle_broadcast
from database.db import init_db
from config import BOT_TOKEN
from celery import Celery

logging.basicConfig(
    filename="bot.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Celery
celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

async def error_handler(update, context):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        with open("assets/error_icon.png", "rb") as f:
            await update.message.reply_photo(
                photo=f,
                caption="An error occurred. Please try again or contact support.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="back")]])
            )

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("balance", lambda update, context: button_callback(update, context, "check_balance")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_broadcast))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(CallbackQueryHandler(handle_admin_callback, pattern="^admin_"))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
