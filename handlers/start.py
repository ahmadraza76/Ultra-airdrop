from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import Session
from database.models import User, ActivityLog
from services.captcha import generate_captcha, generate_captcha_url
from handlers.callback import get_main_menu
import logging
import os

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    referral_id = context.args[0] if context.args else None

    if context.bot_data.get("paused", False):
        await update.message.reply_text("The airdrop is currently paused. Please try again later.")
        return

    try:
        with Session() as session:
            user = session.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                try:
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

                    # Handle referral bonus
                    if referral_id and referral_id != str(user_id):
                        try:
                            referrer = session.query(User).filter_by(telegram_id=int(referral_id)).first()
                            if referrer:
                                referrer.points += 10
                                session.add(ActivityLog(telegram_id=int(referral_id), action="referral_bonus", details=f"Referred user {user_id}"))
                                session.commit()
                        except (ValueError, TypeError):
                            pass  # Invalid referral ID

                    keyboard = [[InlineKeyboardButton("Open CAPTCHA", url=captcha_url)]]
                    
                    # Try to send with banner image
                    banner_path = "assets/banner.jpg"
                    if os.path.exists(banner_path):
                        with open(banner_path, "rb") as f:
                            await update.message.reply_photo(
                                photo=f,
                                caption=f"Welcome to the JHOOM Airdrop Bot! 🎉\n"
                                        f"Please verify you're human by entering the code: **{code}**\n"
                                        f"(CAPTCHA valid for 2 minutes)",
                                parse_mode="Markdown",
                                reply_markup=InlineKeyboardMarkup(keyboard),
                            )
                    else:
                        await update.message.reply_text(
                            f"Welcome to the JHOOM Airdrop Bot! 🎉\n"
                            f"Please verify you're human by entering the code: **{code}**\n"
                            f"(CAPTCHA valid for 2 minutes)",
                            parse_mode="Markdown",
                            reply_markup=InlineKeyboardMarkup(keyboard),
                        )
                    
                    # Send CAPTCHA image if it exists
                    if os.path.exists(image_path) and image_path.endswith(('.png', '.jpg', '.jpeg')):
                        try:
                            with open(image_path, "rb") as f:
                                await update.message.reply_photo(
                                    photo=f,
                                    caption="Enter the code from this CAPTCHA image:",
                                )
                        except Exception as e:
                            logger.error(f"Error sending CAPTCHA image: {e}")
                    
                except Exception as e:
                    logger.error(f"Error in start handler: {e}")
                    await update.message.reply_text(
                        "⚠️ Error generating CAPTCHA. Please try again later.",
                        reply_markup=get_main_menu(),
                    )
            else:
                # User already exists, show main menu
                context.user_data["state"] = "menu"
                banner_path = "assets/banner.jpg"
                if os.path.exists(banner_path):
                    with open(banner_path, "rb") as f:
                        await update.message.reply_photo(
                            photo=f,
                            caption=f"Welcome back to JHOOM Airdrop Bot! 🎉\n"
                                    f"Your current balance: {user.points} JHOOM Points",
                            reply_markup=get_main_menu(),
                        )
                else:
                    await update.message.reply_text(
                        f"Welcome back to JHOOM Airdrop Bot! 🎉\n"
                        f"Your current balance: {user.points} JHOOM Points",
                        reply_markup=get_main_menu(),
                    )
    except Exception as e:
        logger.error(f"Database error in start handler: {e}")
        await update.message.reply_text(
            "⚠️ Database error. Please try again later.",
            reply_markup=get_main_menu(),
        )