#!/bin/bash
# Script to activate virtual environment and run the bot

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated"
echo "🤖 Starting JHOOM Airdrop Bot..."

python run_bot.py