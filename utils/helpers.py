from datetime import datetime
from database.db import Session
from database.models import User, Withdrawal
import pandas as pd
from telegram import Bot
from config import NOTIFY_BOT_TOKEN
from celery import shared_task

@shared_task
def broadcast_message_async(user_ids, message):
    bot = Bot(token=NOTIFY_BOT_TOKEN)
    for user_id in user_ids:
        try:
            bot.send_message(chat_id=user_id, text=f"📢 Broadcast: {message}", parse_mode="Markdown")
        except Exception as e:
            print(f"Broadcast error for {user_id}: {e}")

def export_users():
    with Session() as session:
        users = session.query(User).all()
        data = [{"telegram_id": u.telegram_id, "wallet": u.wallet, "points": u.points, "joined_at": u.joined_at.isoformat(), "tasks_completed": ",".join(u.tasks_completed)} for u in users]
        df = pd.DataFrame(data)
        df.to_excel("users.xlsx", index=False)
        return "users.xlsx"

def notify_user(telegram_id, message):
    bot = Bot(token=NOTIFY_BOT_TOKEN)
    try:
        bot.send_message(chat_id=telegram_id, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"Notification error: {e}")
