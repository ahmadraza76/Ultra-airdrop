from datetime import datetime
from database.db import Session
from database.models import User, Withdrawal
import pandas as pd
from telegram import Bot
from config import NOTIFY_BOT_TOKEN
from celery import shared_task
import asyncio

@shared_task
def broadcast_message_async(user_ids, message):
    """Async task to broadcast message to multiple users"""
    bot = Bot(token=NOTIFY_BOT_TOKEN)
    success_count = 0
    error_count = 0
    
    for user_id in user_ids:
        try:
            # Use asyncio to run the async send_message
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                bot.send_message(
                    chat_id=user_id, 
                    text=f"📢 *Broadcast Message:*\n\n{message}", 
                    parse_mode="Markdown"
                )
            )
            loop.close()
            success_count += 1
        except Exception as e:
            print(f"Broadcast error for {user_id}: {e}")
            error_count += 1
    
    print(f"Broadcast completed: {success_count} successful, {error_count} failed")
    return {"success": success_count, "errors": error_count}

def export_users():
    """Export users to Excel file"""
    with Session() as session:
        users = session.query(User).all()
        data = []
        for u in users:
            data.append({
                "telegram_id": u.telegram_id,
                "wallet": u.wallet or "Not Set",
                "points": u.points,
                "joined_at": u.joined_at.isoformat() if u.joined_at else "Unknown",
                "tasks_completed": len(u.tasks_completed) if u.tasks_completed else 0,
                "task_list": ",".join(u.tasks_completed) if u.tasks_completed else "None",
                "referred_by": u.referred_by or "Direct"
            })
        
        df = pd.DataFrame(data)
        filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        return filename

@shared_task
def notify_user_async(telegram_id, message):
    """Async task to notify a single user"""
    bot = Bot(token=NOTIFY_BOT_TOKEN)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            bot.send_message(chat_id=telegram_id, text=message, parse_mode="Markdown")
        )
        loop.close()
        return True
    except Exception as e:
        print(f"Notification error for {telegram_id}: {e}")
        return False

def notify_user(telegram_id, message):
    """Queue notification task"""
    notify_user_async.delay(telegram_id, message)