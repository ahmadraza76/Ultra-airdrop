import os
import random
import string
import redis
import time
import logging
from config import REDIS_URL, BASE_URL
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Initialize Redis connection with retry mechanism
def connect_redis_with_retry(max_retries=5, delay=2):
    """Connect to Redis with retry mechanism"""
    for attempt in range(max_retries):
        try:
            r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
            r.ping()
            logger.info("Redis connection established successfully")
            return r
        except redis.ConnectionError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Redis connection attempt {attempt + 1} failed, retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.warning("Redis connection failed after all retries. CAPTCHA functionality may not work.")
                return None
    return None

r = connect_redis_with_retry()

CAPTCHA_DIR = "assets/captcha_images"
CAPTCHA_TTL = 120  # 2 minutes

def generate_captcha(user_id):
    """Generate CAPTCHA for user"""
    # Create captcha directory if it doesn't exist
    os.makedirs(CAPTCHA_DIR, exist_ok=True)
    
    # Get available captcha images
    files = [f for f in os.listdir(CAPTCHA_DIR) if f.endswith((".png", ".jpg", ".jpeg"))]
    
    if not files:
        # Create a simple text-based captcha if no images exist
        dummy_path = os.path.join(CAPTCHA_DIR, "text_captcha.txt")
        code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        with open(dummy_path, "w") as f:
            f.write(f"CAPTCHA Code: {code}")
        image_path = dummy_path
    else:
        image = random.choice(files)
        image_path = os.path.join(CAPTCHA_DIR, image)
        code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    
    # Store in Redis if available
    if r:
        key = f"captcha:{user_id}"
        r.setex(key, CAPTCHA_TTL, code)
    
    return image_path, code

def verify_captcha(user_id, input_code):
    """Verify CAPTCHA code"""
    if not r:
        # Fallback: accept any 6-character code if Redis is not available
        return len(input_code) == 6
    
    key = f"captcha:{user_id}"
    stored_code = r.get(key)
    
    if stored_code:
        correct = stored_code.lower() == input_code.lower()
        if correct:
            r.delete(key)  # Only delete if correct
        return correct
    return False

def generate_captcha_url(user_id):
    """Generate CAPTCHA URL for web verification"""
    code = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    
    if r:
        key = f"captcha_url:{user_id}"
        r.setex(key, CAPTCHA_TTL, code)
    
    return f"{BASE_URL}/captcha/{user_id}/{code}"