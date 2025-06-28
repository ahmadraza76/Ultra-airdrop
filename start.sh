#!/bin/bash

echo "🚀 Starting JHOOM Airdrop Bot Setup..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs assets assets/captcha_images data

# Copy .env file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from template"
        echo "⚠️  Please edit .env file with your actual values"
    else
        echo "❌ .env.example not found"
    fi
fi

# Create dummy assets
echo "Creating dummy assets..."
python assets/create_dummy_images.py

# Start Redis if available
if command -v redis-server &> /dev/null; then
    echo "Starting Redis server..."
    redis-server --daemonize yes
else
    echo "⚠️  Redis not found. Please install Redis for full functionality."
fi

echo "🎉 Setup complete!"
echo "📝 Next steps:"
echo "1. Edit .env file with your bot tokens and configuration"
echo "2. Replace credentials.json with your Google Service Account credentials"
echo "3. Replace dummy images in assets/ with your actual images"
echo "4. Run: python run_bot.py"