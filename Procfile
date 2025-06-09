web: gunicorn -w 4 -b 0.0.0.0:$PORT captcha_server:app
worker: celery -A bot.celery worker --loglevel=info
bot: python bot.py
