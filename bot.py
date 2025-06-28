import logging
import os
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.start import start
from handlers.message import handle_message
from handlers.callback import button_callback
from handlers.admin import admin, handle_admin_callback, handle_broadcast
from database.db import init_db
from config import BOT_TOKEN, validate_config
from celery import Celery

# Create necessary directories first
os.makedirs("logs", exist_ok=True)
os.makedirs("assets", exist_ok=True)
os.makedirs("assets/captcha_images", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Celery
celery = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
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
        try:
            if os.path.exists("assets/error_icon.png"):
                with open("assets/error_icon.png", "rb") as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption="An error occurred. Please try again or contact support.",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="back")]])
                    )
            else:
                await update.message.reply_text(
                    "⚠️ An error occurred. Please try again or contact support.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="back")]])
                )
        except Exception as e:
            logger.error(f"Error in error handler: {e}")

def main():
    # Validate configuration
    if not validate_config():
        sys.exit(1)
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("balance", lambda update, context: button_callback(update, context)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^(?!admin_)"))
    app.add_handler(CallbackQueryHandler(handle_admin_callback, pattern="^admin_"))
    app.add_error_handler(error_handler)

    logger.info("Bot started successfully")
    app.run_polling()

if __name__ == "__main__":
    main()