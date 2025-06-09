from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import Session
from database.models import User, ActivityLog, Withdrawal
from config import TASKS, TELEGRAM_CHANNEL, TELEGRAM_GROUP, FAQS
from services.telegram_api import verify_tasks
from services.google_sheet import save_withdrawal
from utils.rate_limiter import rate_limit
from random import random, randint
from datetime import datetime

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("Join Airdrop", callback_data="join_airdrop")],
        [InlineKeyboardButton("Check Balance", callback_data="check_balance")],
        [InlineKeyboardButton("Referral Link", callback_data="referral_link")],
        [InlineKeyboardButton("Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("Bonus", callback_data="bonus")],
        [InlineKeyboardButton("Task List", callback_data="task_list")],
        [InlineKeyboardButton("FAQ", callback_data="faq")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="back")]])

async def start_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    context.user_data["onboarding_step"] = 0
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user.wallet:
            await update.message.reply_text(
                "📚 *Onboarding Step 1: Set Up Wallet*\n\n"
                "Please enter a valid BEP-20 or ERC-20 wallet address to receive JHOOM Points.",
                parse_mode="Markdown",
                reply_markup=get_back_button(),
            )
            context.user_data["state"] = "wallet"
        else:
            context.user_data["onboarding_step"] = 1
            await update.message.reply_text(
                "📚 *Onboarding Step 2: Complete Tasks*\n\n"
                "Earn JHOOM Points by completing tasks like joining our Telegram channel or following us on Twitter.\n"
                "Click below to view tasks.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("View Tasks", callback_data="task_list")]])
            )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if context.bot_data.get("paused", False) and not query.data.startswith("admin_"):
        with open("assets/error_icon.png", "rb") as f:
            await query.message.reply_photo(
                photo=f,
                caption="The airdrop is currently paused. Please try again later.",
                reply_markup=get_back_button(),
            )
        return

    with Session() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        if not user:
            with open("assets/error_icon.png", "rb") as f:
                await query.message.reply_photo(
                    photo=f,
                    caption="Please start the bot with /start",
                    reply_markup=get_back_button(),
                )
            return

        data = query.data
        if data == "join_airdrop":
            if user.wallet:
                with open("assets/error_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption="You have already joined the airdrop! Check tasks or balance.",
                        reply_markup=get_main_menu(),
                    )
            else:
                context.user_data["state"] = "wallet"
                await query.message.reply_text(
                    "Please enter your BEP-20 or ERC-20 wallet address to join the airdrop.",
                    reply_markup=get_back_button(),
                )
        elif data == "check_balance":
            with open("assets/success_icon.png", "rb") as f:
                await query.message.reply_photo(
                    photo=f,
                    caption=f"Your balance: *{user.points} JHOOM Points* 💰",
                    parse_mode="Markdown",
                    reply_markup=get_main_menu(),
                )
        elif data == "referral_link":
            link = f"https://t.me/{context.bot.username}?start={user_id}"
            with open("assets/success_icon.png", "rb") as f:
                await query.message.reply_photo(
                    photo=f,
                    caption=f"Your referral link: {link}\nInvite friends to earn 10 JHOOM Points per referral! 🚀",
                    reply_markup=get_main_menu(),
                )
        elif data == "withdraw":
            if not rate_limit(user_id, "withdraw", limit=1, window=3600):
                with open("assets/error_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption="You can only request a withdrawal once per hour. Try again later! ⏳",
                        reply_markup=get_main_menu(),
                    )
                return
            if user.points >= 100:
                keyboard = [[InlineKeyboardButton("Request Withdrawal", callback_data="confirm_withdraw")]]
                with open("assets/withdrawal_banner.jpg", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption=f"You're eligible for withdrawal!\n\n"
                                f"Wallet: {user.wallet}\n"
                                f"Amount: {user.points} JHOOM Points\n\n"
                                "Confirm your request:",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                    )
            else:
                with open("assets/error_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption="You need at least 100 JHOOM Points to withdraw. Keep earning! 💪",
                        reply_markup=get_main_menu(),
                    )
        elif data == "confirm_withdraw":
            withdrawal = Withdrawal(
                telegram_id=user_id,
                wallet=user.wallet,
                amount=user.points,
            )
            user.points = 0
            session.add(withdrawal)
            session.add(ActivityLog(telegram_id=user_id, action="withdraw_request", details=f"Requested {withdrawal.amount} JHOOM Points"))
            session.commit()
            save_withdrawal(user_id, user.wallet, withdrawal.amount, withdrawal.requested_at)
            with open("assets/withdrawal_banner.jpg", "rb") as f:
                await query.message.reply_photo(
                    photo=f,
                    caption="Your withdrawal request has been submitted. You'll receive your tokens within 24 hours. ✅",
                    reply_markup=get_main_menu(),
                )
        elif data == "bonus":
            if not rate_limit(user_id, "bonus", limit=1, window=3600):
                with open("assets/error_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption="You can claim a bonus once per hour. Try again later! ⏳",
                        reply_markup=get_main_menu(),
                    )
                return
            user.last_bonus = datetime.utcnow()
            if random() < 0.3:
                bonus = randint(5, 20)
                user.points += bonus
                session.add(ActivityLog(telegram_id=user_id, action="bonus", details=f"Earned {bonus} JHOOM Points"))
                session.commit()
                with open("assets/success_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption=f"Congratulations! You earned a bonus of {bonus} JHOOM Points! 🎁",
                        reply_markup=get_main_menu(),
                    )
            else:
                with open("assets/error_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption="No bonus this time. Try again later! 😊",
                        reply_markup=get_main_menu(),
                    )
        elif data == "task_list":
            task_status = await verify_tasks(context, user_id)
            for i, task in enumerate(TASKS[:2]):
                if (i == 0 and task_status[TELEGRAM_CHANNEL]) or (i == 1 and task_status[TELEGRAM_GROUP]):
                    if task["description"] not in user.tasks_completed:
                        user.tasks_completed.append(task["description"])
                        user.points += 10
                        session.add(ActivityLog(telegram_id=user_id, action="task_completed", details=f"Task: {task['description']}"))
                        session.commit()
            task_list = "\n".join([f"☑️ {task['description']} [Video Guide]({task['video']})" if task['description'] in user.tasks_completed else f"⬜ {task['description']} [Video Guide]({task['video']})" for task in TASKS])
            progress = f"Progress: {len(user.tasks_completed)} of {len(TASKS)} tasks completed"
            keyboard = [[InlineKeyboardButton(f"Complete Task {i+1}", callback_data=f"complete_task_{i}")] for i in range(2, len(TASKS))]
            keyboard.append([InlineKeyboardButton("Back to Menu", callback_data="back")])
            with open("assets/tasks_banner.jpg", "rb") as f:
                await query.message.reply_photo(
                    photo=f,
                    caption=f"📋 Airdrop Tasks:\n{task_list}\n\n{progress}\n\nSelect a task to mark as completed (Telegram tasks are auto-verified):",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                )
        elif data.startswith("complete_task_"):
            task_idx = int(data.split("_")[-1])
            if task_idx < 2:
                with open("assets/error_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption="Telegram tasks are auto-verified. Please join the channel/group.",
                        reply_markup=get_main_menu(),
                    )
                return
            if TASKS[task_idx]["description"] not in user.tasks_completed:
                user.tasks_completed.append(TASKS[task_idx]["description"])
                user.points += 10
                session.add(ActivityLog(telegram_id=user_id, action="task_completed", details=f"Task: {TASKS[task_idx]['description']}"))
                session.commit()
                with open("assets/success_icon.png", "rb") as f:
                    await query.message.reply_photo(
                        photo=f,
                        caption=f"Task '{TASKS[task_idx]['description']}' marked as completed! +10 JHOOM Points. 🎉",
                        reply_markup=get_main_menu(),
                    )
            else:
                with open("assets/error_icon.png", "rb") as f:
                    query.message.reply_photo(
                        photo=f,
                        caption="This task is already completed! Choose another.",
                        reply_markup=get_main_menu(),
                    )
        elif data == "faq":
            faq_text = "\n\n".join([f"❓ *{faq['question']}*\n{faq['answer']}" for faq in FAQS])
            await query.message.reply_text(
                f"📖 *FAQ*\n\n{faq_text}",
                parse_mode="Markdown",
                reply_markup=get_main_menu(),
            )
        elif data == "help":
            await query.message.reply_text(
                "ℹ️ *JHOOM Airdrop Bot Help Center*\n\n"
                "Follow these steps to participate:\n"
                "1. *Verify CAPTCHA*: Enter the code from the image.\n"
                "2. *Set Up Wallet*: Submit a BEP-20/ERC-20 address.\n"
                "3. *Complete Tasks*: Earn JHOOM Points by joining channels or social media.\n"
                "4. *Invite Friends*: Share your referral link for 10 points per friend.\n"
                "5. *Withdraw*: Request withdrawal (min 100 points) to receive tokens.\n"
                "6. *Check Balance*: Use the Check Balance button or /balance.\n\n"
                "Need help? Check the FAQ or contact support: @JHOOMSupport",
                parse_mode="Markdown",
                reply_markup=get_main_menu(),
            )
        elif data == "onboarding_next":
            step = context.user_data.get("onboarding_step", 0) + 1
            context.user_data["onboarding_step"] = step
            if step == 1:
                await query.message.reply_text(
                    "📚 *Onboarding Step 2: Complete Tasks*\n\n"
                    "Earn JHOOM Points by completing tasks like joining our Telegram channel or following us on Twitter.\n"
                    "Click below to view tasks.",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("View Tasks", callback_data="task_list")]])
                )
            elif step == 2:
                await query.message.reply_text(
                    "📚 *Onboarding Step 3: Invite Friends*\n\n"
                    "Share your referral link to earn 10 JHOOM Points per friend who joins.\n"
                    "Click below to get your link.",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Get Referral Link", callback_data="referral_link")]])
                )
            else:
                context.user_data["state"] = "menu"
                await query.message.reply_text(
                    "🎉 *Onboarding Complete!*\n\n"
                    "You're ready to earn more JHOOM Points. Use the menu to explore.",
                    parse_mode="Markdown",
                    reply_markup=get_main_menu(),
                )
        elif data == "back":
            context.user_data["state"] = "menu"
            await query.message.reply_text(
                "Back to main menu.", reply_markup=get_main_menu()
            )
