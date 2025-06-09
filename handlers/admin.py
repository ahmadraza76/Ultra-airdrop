from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import Session
from database.models import User, ActivityLog, Withdrawal
from config import ADMIN_IDS
from utils.helpers import export_users, broadcast_message_async

def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton("View Stats", callback_data="admin_stats")],
        [InlineKeyboardButton("Broadcast Message", callback_data="admin_broadcast")],
        [InlineKeyboardButton("Pause/Unpause Airdrop", callback_data="admin_pause")],
        [InlineKeyboardButton("Export Users", callback_data="admin_export")],
        [InlineKeyboardButton("View Logs", callback_data="admin_logs")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMIN_IDS:
        await update.message.reply_text(
            "Welcome to the Admin Panel!", reply_markup=get_admin_menu()
        )
    else:
        with open("assets/error_icon.png", "rb") as f:
            await update.message.reply_photo(
                photo=f,
                caption="Unauthorized access.",
                reply_markup=get_main_menu(),
            )

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in ADMIN_IDS:
        with open("assets/error_icon.png", "rb") as f:
            await query.message.reply_photo(
                photo=f,
                caption="Unauthorized access.",
                reply_markup=get_admin_menu(),
            )
        return

    data = query.data
    with Session() as session:
        if data == "admin_stats":
            users = session.query(User).all()
            withdrawals = session.query(Withdrawal).filter_by(status="Pending").count()
            total_points = sum(user.points for user in users)
            await query.message.reply_text(
                f"📊 Bot Stats:\nTotal Users: {len(users)}\nPending Withdrawals: {withdrawals}\nTotal JHOOM Points: {total_points}",
                reply_markup=get_admin_menu(),
            )
        elif data == "admin_broadcast":
            context.user_data["state"] = "broadcast"
            await query.message.reply_text(
                "Enter the message to broadcast to all users (max 4096 characters):",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Menu", callback_data="back")]])
            )
        elif data == "admin_pause":
            context.bot_data["paused"] = not context.bot_data.get("paused", False)
            status = "paused" if context.bot_data["paused"] else "unpaused"
            await query.message.reply_text(
                f"Airdrop {status}!", reply_markup=get_admin_menu()
            )
        elif data == "admin_export":
            filename = export_users()
            await context.bot.send_document(
                chat_id=user_id,
                document=open(filename, "rb"),
                caption="Exported user data (Excel)",
                reply_markup=get_admin_menu(),
            )
        elif data == "admin_logs":
            logs = session.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(50).all()
            log_text = "\n".join([f"{log.timestamp}: {log.action} by {log.telegram_id} - {log.details}" for log in logs])
            await query.message.reply_text(
                f"📜 Recent Activity Logs:\n{log_text or 'No logs available.'}",
                reply_markup=get_admin_menu(),
            )

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS or context.user_data.get("state") != "broadcast":
        return

    message = update.message.text
    if len(message) > 4096:
        with open("assets/error_icon.png", "rb") as f:
            await update.message.reply_photo(
                photo=f,
                caption="Message too long! Please keep it under 4096 characters.",
                reply_markup=get_admin_menu(),
            )
        return

    context.user_data["state"] = "menu"
    with Session() as session:
        users = session.query(User).all()
        user_ids = [user.telegram_id for user in users]
        broadcast_message_async.delay(user_ids, message)
        session.add(ActivityLog(telegram_id=user_id, action="broadcast", details=f"Sent: {message[:50]}..."))
        session.commit()
    await update.message.reply_text(
        "Broadcast queued for all users!", reply_markup=get_admin_menu()
    )
