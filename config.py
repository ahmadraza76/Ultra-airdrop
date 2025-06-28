import os
from dotenv import load_dotenv

load_dotenv()

# Required environment variables with defaults
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GOOGLE_SHEET_KEY = os.getenv("GOOGLE_SHEET_KEY", "")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE", "credentials.json")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
NOTIFY_BOT_TOKEN = os.getenv("NOTIFY_BOT_TOKEN", "")
BASE_URL = os.getenv("BASE_URL", "https://localhost:8000")

# Parse admin IDs safely
admin_ids_str = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = []
if admin_ids_str:
    try:
        ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(",") if id.strip()]
    except ValueError:
        print("Warning: Invalid ADMIN_IDS format in .env file")

TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@your_channel")
TELEGRAM_GROUP = os.getenv("TELEGRAM_GROUP", "@your_group")

# Validate required configuration
def validate_config():
    missing = []
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not ADMIN_IDS:
        missing.append("ADMIN_IDS")
    
    if missing:
        print(f"❌ Missing required configuration: {', '.join(missing)}")
        print("Please check your .env file")
        return False
    return True

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