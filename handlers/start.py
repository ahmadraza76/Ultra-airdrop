from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import Session
from database.models import User, ActivityLog
from services.captcha import generate_captcha, generate_captcha_url
from handlers.callback import get_main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    referral_id = context.args[0] if context.args else None

    if context.bot_data.get("paused", False):
        await update.message.reply_text("The airdrop is currently paused. Please try again later.")
        return

    with Session() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            image_path, code = generate_captcha(user_id)
            captcha_url = generate_captcha_url(user_id)
            user = User(
                telegram_id=user_id,
                referred_by=referral_id,
                tasks_completed=[],
            )
            context.user_data["captcha"] = code
            context.user_data["state"] = "captcha"
            session.add(user)
            session.add(ActivityLog(telegram_id=user_id, action="start", details="Started bot"))
            session.commit()

            if referral_id and referral_id != str(user_id):
                referrer = session.query(User).filter_by(telegram_id=int(referral_id)).first()
                if referrer:
                    referrer.points += 10
                    session.add(ActivityLog(telegram_id=int(referral_id), action="referral_bonus", details=f"Referred user {user_id}"))
                    session.commit()

        keyboard = [[InlineKeyboardButton("Open CAPTCHA", url=captcha_url)]]
        with open("assets/banner.jpg", "rb") as f:
            await update.message.reply_photo(
                photo=f,
                caption=f"Welcome to the JHOOM Airdrop Bot! 🎉\n"
                        f"Please verify you're human by entering the code in the CAPTCHA (valid for 2 minutes):",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        with open(image_path, "rb") as f:
            await update.message.reply_photo(
                photo=f,
                reply_markup=get_main_menu(),
            )
