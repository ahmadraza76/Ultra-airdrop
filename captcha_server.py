from flask import Flask, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
from services.captcha import generate_captcha
from config import REDIS_URL

app = Flask(__name__)
r = redis.Redis.from_url(REDIS_URL)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per minute"],
    storage_uri=REDIS_URL
)

@app.route("/captcha/<user_id>/<code>")
@limiter.limit("5/minute")
def captcha_page(user_id, code):
    if r.get(f"captcha_url:{user_id}") == code.encode():
        image, _ = generate_captcha(user_id)
        return send_file(image, mimetype="image/png")
    return "Invalid or expired CAPTCHA", 403

if __name__ == "__main__":
    # Use gunicorn for production: gunicorn -w 4 -b 0.0.0.0:8000 captcha_server:app
    app.run(ssl_context="adhoc")  # Local testing with HTTPS
