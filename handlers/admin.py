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
        [InlineKeyboardButton("Back to Menu", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_menu():
    from handlers.callback import get_main_menu as get_main
    return get_main()

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMIN_IDS:
        await update.message.reply_text(
            "🔧 Welcome to the Admin Panel!", reply_markup=get_admin_menu()
        )
    else:
        try:
            with open("assets/error_icon.png", "rb") as f:
                await update.message.reply_photo(
                    photo=f,
                    caption="⚠️ Unauthorized access.",
                    reply_markup=get_main_menu(),
                )
        except FileNotFoundError:
            await update.message.reply_text(
                "⚠️ Unauthorized access.",
                reply_markup=get_main_menu(),
            )

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in ADMIN_IDS:
        try:
            with open("assets/error_icon.png", "rb") as f:
                await query.message.reply_photo(
                    photo=f,
                    caption="⚠️ Unauthorized access.",
                    reply_markup=get_admin_menu(),
                )
        except FileNotFoundError:
            await query.message.reply_text(
                "⚠️ Unauthorized access.",
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
                f"📊 *Bot Statistics:*\n\n"
                f"👥 Total Users: {len(users)}\n"
                f"⏳ Pending Withdrawals: {withdrawals}\n"
                f"💰 Total JHOOM Points: {total_points:.2f}\n"
                f"✅ Active Users: {len([u for u in users if u.wallet])}\n"
                f"📈 Users with Points: {len([u for u in users if u.points > 0])}",
                parse_mode="Markdown",
                reply_markup=get_admin_menu(),
            )
        elif data == "admin_broadcast":
            context.user_data["state"] = "broadcast"
            await query.message.reply_text(
                "📢 *Broadcast Message*\n\n"
                "Enter the message to broadcast to all users (max 4096 characters):",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="admin_stats")]])
            )
        elif data == "admin_pause":
            context.bot_data["paused"] = not context.bot_data.get("paused", False)
            status = "⏸️ PAUSED" if context.bot_data["paused"] else "▶️ ACTIVE"
            await query.message.reply_text(
                f"🔄 Airdrop status changed to: {status}",
                reply_markup=get_admin_menu()
            )
        elif data == "admin_export":
            try:
                filename = export_users()
                with open(filename, "rb") as f:
                    await context.bot.send_document(
                        chat_id=user_id,
                        document=f,
                        caption="📊 Exported user data (Excel format)",
                        reply_markup=get_admin_menu(),
                    )
            except Exception as e:
                await query.message.reply_text(
                    f"⚠️ Error exporting users: {str(e)}",
                    reply_markup=get_admin_menu(),
                )
        elif data == "admin_logs":
            logs = session.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(20).all()
            if logs:
                log_text = "\n".join([f"🕐 {log.timestamp.strftime('%Y-%m-%d %H:%M')}: {log.action} by {log.telegram_id}" for log in logs])
                await query.message.reply_text(
                    f"📜 *Recent Activity Logs:*\n\n{log_text}",
                    parse_mode="Markdown",
                    reply_markup=get_admin_menu(),
                )
            else:
                await query.message.reply_text(
                    "📜 No activity logs available.",
                    reply_markup=get_admin_menu(),
                )

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS or context.user_data.get("state") != "broadcast":
        return

    message = update.message.text
    if len(message) > 4096:
        try:
            with open("assets/error_icon.png", "rb") as f:
                await update.message.reply_photo(
                    photo=f,
                    caption="⚠️ Message too long! Please keep it under 4096 characters.",
                    reply_markup=get_admin_menu(),
                )
        except FileNotFoundError:
            await update.message.reply_text(
                "⚠️ Message too long! Please keep it under 4096 characters.",
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
        f"📢 Broadcast queued for {len(user_ids)} users!",
        reply_markup=get_admin_menu()
    )