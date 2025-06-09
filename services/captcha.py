import os
import random
import string
import redis
from config import REDIS_URL
from datetime import datetime, timedelta

r = redis.Redis.from_url(REDIS_URL)
CAPTCHA_DIR = "assets/captcha_images"
CAPTCHA_TTL = 120  # 2 minutes

def generate_captcha(user_id):
    files = [f for f in os.listdir(CAPTCHA_DIR) if f.endswith(".png")]
    if not files:
        raise FileNotFoundError("No CAPTCHA images found")
    image = random.choice(files)
    code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    key = f"captcha:{user_id}"
    r.setex(key, CAPTCHA_TTL, code)
    return os.path.join(CAPTCHA_DIR, image), code

def verify_captcha(user_id, input_code):
    key = f"captcha:{user_id}"
    stored_code = r.get(key)
    if stored_code:
        correct = stored_code.decode().lower() == input_code.lower()
        r.delete(key)
        return correct
    return False

def generate_captcha_url(user_id):
    from config import BASE_URL
    code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    key = f"captcha_url:{user_id}"
    r.setex(key, CAPTCHA_TTL, code)
    return f"{BASE_URL}/captcha/{user_id}/{code}"
