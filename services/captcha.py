import os
import random
import string
import redis
from config import REDIS_URL, BASE_URL
from datetime import datetime, timedelta

r = redis.Redis.from_url(REDIS_URL)
CAPTCHA_DIR = "assets/captcha_images"
CAPTCHA_TTL = 120  # 2 minutes

def generate_captcha(user_id):
    # Create captcha directory if it doesn't exist
    os.makedirs(CAPTCHA_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(CAPTCHA_DIR) if f.endswith((".png", ".jpg", ".jpeg"))]
    if not files:
        # Create a dummy captcha file if none exist
        dummy_path = os.path.join(CAPTCHA_DIR, "dummy_captcha.png")
        with open(dummy_path, "w") as f:
            f.write("dummy captcha file")
        files = ["dummy_captcha.png"]
    
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
        if correct:
            r.delete(key)  # Only delete if correct
        return correct
    return False

def generate_captcha_url(user_id):
    code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    key = f"captcha_url:{user_id}"
    r.setex(key, CAPTCHA_TTL, code)
    return f"{BASE_URL}/captcha/{user_id}/{code}"