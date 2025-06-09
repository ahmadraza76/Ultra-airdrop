import redis
from config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

def rate_limit(user_id, action, limit=1, window=3600):
    key = f"rate_limit:{user_id}:{action}"
    count = r.get(key)
    if count and int(count) >= limit:
        return False
    if not count:
        r.setex(key, window, 1)
    else:
        r.incr(key)
    return True
