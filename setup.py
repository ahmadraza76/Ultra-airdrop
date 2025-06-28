#!/usr/bin/env python3
"""
Setup script to initialize the bot environment
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        "assets",
        "assets/captcha_images",
        "logs",
        "data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your actual values")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env file already exists")

def create_dummy_assets():
    """Create dummy asset files"""
    print("Creating dummy assets...")
    try:
        subprocess.check_call([sys.executable, "assets/create_dummy_images.py"])
        print("✅ Dummy assets created")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating dummy assets: {e}")
    except FileNotFoundError:
        print("⚠️  PIL not installed, skipping dummy image creation")

def create_credentials_template():
    """Create credentials.json template"""
    credentials_template = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
    }
    
    if not os.path.exists("credentials.json"):
        import json
        with open("credentials.json", "w") as f:
            json.dump(credentials_template, f, indent=2)
        print("✅ Created credentials.json template")
        print("⚠️  Please replace with your actual Google Service Account credentials")
    else:
        print("✅ credentials.json already exists")

def main():
    print("🚀 Setting up JHOOM Airdrop Bot...")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Create credentials template
    create_credentials_template()
    
    # Create dummy assets
    create_dummy_assets()
    
    print("\n🎉 Setup completed!")
    print("\n📝 Next steps:")
    print("1. Edit .env file with your bot tokens and configuration")
    print("2. Replace credentials.json with your Google Service Account credentials")
    print("3. Replace dummy images in assets/ with your actual images")
    print("4. Start Redis server: redis-server")
    print("5. Run the bot: python bot.py")

if __name__ == "__main__":
    main()