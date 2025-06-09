from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import Session
from database.models import User, ActivityLog
from services.captcha import verify_captcha, generate_captcha, generate_captcha_url
from services.wallet_check import is_valid_wallet
from services.google_sheet import save_user
from handlers.callback import get_main_menu, start_onboarding

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if context.bot_data.get("paused", False):
        await update.message.reply_text("The airdrop is currently paused. Please try again later.")
        return

    with Session() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            await update.message.reply_text("Please start the bot with /start")
            return

        state = context.user_data.get("state", "menu")
        if state == "captcha":
            if verify_captcha(user_id, text):
                context.user_data["state"] = "onboarding"
                session.add(ActivityLog(telegram_id=user_id, action="captcha_verified", details="Passed CAPTCHA"))
                session.commit()
                await start_onboarding(update, context)
            else:
                image_path, code = generate_captcha(user_id)
                captcha_url = generate_captcha_url(user_id)
                context.user_data["captcha"] = code
                session.add(ActivityLog(telegram_id=user_id, action="captcha_failed", details="Failed CAPTCHA"))
                session.commit()
                keyboard = [[InlineKeyboardButton("Open CAPTCHA", url=captcha_url)]]
                with open("assets/error_icon.png", "rb") as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption=f"Incorrect captcha. Please try again with this new CAPTCHA (valid for 2 minutes):",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                    )
                with open(image_path, "rb") as f:
                    await update.message.reply_photo(photo=f)
        elif state == "wallet":
            if is_valid_wallet(text):
                user.wallet = text
                user.points += 50
                context.user_data["state"] = "onboarding"
                session.add(ActivityLog(telegram_id=user_id, action="wallet_added", details=f"Wallet: {text}"))
                session.commit()
                save_user(user_id, text, user.points, user.joined_at)
                with open("assets/success_icon.png", "rb") as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption="Wallet address saved! 🎉 You earned 50 JHOOM Points.\n"
                                "Let's continue with the next step.",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Next Step", callback_data="onboarding_next")]])
                    )
            else:
                with open("assets/error_icon.png", "rb") as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption="Invalid BEP-20/ERC-20 address. Please enter a valid wallet address.",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="back")]])
                    )
