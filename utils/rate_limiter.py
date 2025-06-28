import redis
from config import REDIS_URL
import time
import logging

logger = logging.getLogger(__name__)

# Initialize Redis connection with error handling
try:
    r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()
except redis.ConnectionError:
    logger.warning("Redis connection failed. Rate limiting will use in-memory fallback.")
    r = None

# In-memory fallback for rate limiting
_memory_store = {}

def rate_limit(user_id, action, limit=1, window=3600):
    """Rate limit user actions"""
    key = f"rate_limit:{user_id}:{action}"
    current_time = int(time.time())
    
    if r:
        # Use Redis if available
        try:
            count = r.get(key)
            if count and int(count) >= limit:
                return False
            if not count:
                r.setex(key, window, 1)
            else:
                r.incr(key)
            return True
        except Exception as e:
            logger.error(f"Redis rate limit error: {e}")
            # Fall through to memory store
    
    # In-memory fallback
    if key in _memory_store:
        last_time, count = _memory_store[key]
        if current_time - last_time > window:
            # Reset window
            _memory_store[key] = (current_time, 1)
            return True
        elif count >= limit:
            return False
        else:
            _memory_store[key] = (last_time, count + 1)
            return True
    else:
        _memory_store[key] = (current_time, 1)
        return True