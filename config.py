import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_SHEET_KEY = os.getenv("GOOGLE_SHEET_KEY")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS").split(",")]
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL")
TELEGRAM_GROUP = os.getenv("TELEGRAM_GROUP")
REDIS_URL = os.getenv("REDIS_URL")
NOTIFY_BOT_TOKEN = os.getenv("NOTIFY_BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

TASKS = [
    {
        "description": f"Join our Telegram Channel: {TELEGRAM_CHANNEL}",
        "video": "https://youtube.com/task1-guide"
    },
    {
        "description": f"Join our Telegram Group: {TELEGRAM_GROUP}",
        "video": "https://youtube.com/task2-guide"
    },
    {
        "description": "Follow us on Twitter: twitter.com/YourTwitter",
        "video": "https://youtube.com/task3-guide"
    },
    {
        "description": "Like our Facebook Page: facebook.com/YourFacebook",
        "video": "https://youtube.com/task4-guide"
    },
]

FAQS = [
    {
        "question": "How do I join the airdrop?",
        "answer": "Use /start, verify the CAPTCHA, and submit a wallet address."
    },
    {
        "question": "What are JHOOM Points?",
        "answer": "Points you earn for tasks, redeemable for tokens via withdrawal."
    },
    {
        "question": "How do I withdraw?",
        "answer": "Earn 100+ points, click Withdraw, and wait for admin processing."
    }
]
