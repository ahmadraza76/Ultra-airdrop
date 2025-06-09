from telegram.error import TelegramError
from config import TELEGRAM_CHANNEL, TELEGRAM_GROUP

async def verify_telegram_membership(context, user_id, chat_id):
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramError:
        return False

async def verify_tasks(context, user_id):
    channel_joined = await verify_telegram_membership(context, user_id, TELEGRAM_CHANNEL)
    group_joined = await verify_telegram_membership(context, user_id, TELEGRAM_GROUP)
    return {
        TELEGRAM_CHANNEL: channel_joined,
        TELEGRAM_GROUP: group_joined,
    }
