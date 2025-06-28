#!/usr/bin/env python3
"""
Main script to run the JHOOM Airdrop Bot
This script handles setup and starts the bot
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_redis():
    """Check if Redis is running"""
    try:
        import redis
        r = redis.Redis.from_url("redis://localhost:6379/0")
        r.ping()
        print("✅ Redis is running")
        return True
    except Exception:
        print("❌ Redis is not running")
        return False

def start_redis():
    """Try to start Redis server"""
    try:
        subprocess.Popen(["redis-server"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)  # Wait for Redis to start
        return check_redis()
    except FileNotFoundError:
        print("❌ Redis server not found. Please install Redis.")
        return False

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import telegram
        import sqlalchemy
        import redis
        import gspread
        import celery
        import flask
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        return False

def setup_environment():
    """Setup the environment"""
    # Create necessary directories
    directories = ["logs", "assets", "assets/captcha_images", "data"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Check .env file
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please create it from .env.example")
        return False
    
    print("✅ Environment setup complete")
    return True

def main():
    print("🚀 Starting JHOOM Airdrop Bot...")
    
    # Check requirements
    if not check_requirements():
        print("Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return
    
    # Setup environment
    if not setup_environment():
        return
    
    # Check Redis
    if not check_redis():
        print("Trying to start Redis...")
        if not start_redis():
            print("⚠️  Redis is not available. Some features may not work.")
    
    # Start the bot
    print("🤖 Starting Telegram bot...")
    try:
        from bot import main as bot_main
        bot_main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    main()