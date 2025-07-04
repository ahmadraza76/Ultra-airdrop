#!/usr/bin/env python3
"""
🚀 JHOOM Airdrop Bot - Professional Telegram Bot
Main script to run the JHOOM Airdrop Bot with proper setup and error handling

Developed by [Your Name] - Professional Bot Developer
"""

import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 JHOOM AIRDROP BOT 🚀                   ║
    ║                                                              ║
    ║              Professional Telegram Airdrop Bot              ║
    ║                   with Advanced Features                    ║
    ║                                                              ║
    ║              Developed by [Your Name]                       ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8+ is required. Current version: %s", sys.version)
        return False
    logger.info("✅ Python version: %s", sys.version.split()[0])
    return True

def check_virtual_env():
    """Check if running in virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        logger.info("✅ Running in virtual environment")
        return True
    else:
        logger.warning("⚠️  Not running in virtual environment")
        logger.info("💡 Consider using: source venv/bin/activate")
        return False

def get_pip_command():
    """Get the correct pip command for the current Python environment"""
    # Try different pip commands in order of preference
    pip_commands = [
        [sys.executable, "-m", "pip"],  # Most reliable
        ["pip3"],
        ["pip"],
        ["python3", "-m", "pip"],
        ["python", "-m", "pip"]
    ]
    
    for cmd in pip_commands:
        try:
            result = subprocess.run(
                cmd + ["--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                logger.info("✅ Using pip command: %s", " ".join(cmd))
                return cmd
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            continue
    
    logger.error("❌ No working pip command found")
    return None

def check_redis():
    """Check if Redis is running"""
    try:
        import redis
        r = redis.Redis.from_url("redis://localhost:6379/0")
        r.ping()
        logger.info("✅ Redis is running")
        return True
    except ImportError:
        logger.warning("⚠️  Redis module not installed")
        return False
    except Exception as e:
        logger.warning("⚠️  Redis is not running: %s", e)
        return False

def start_redis():
    """Try to start Redis server"""
    try:
        logger.info("🔄 Attempting to start Redis server...")
        subprocess.Popen(
            ["redis-server"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        time.sleep(3)  # Wait for Redis to start
        return check_redis()
    except FileNotFoundError:
        logger.warning("❌ Redis server not found. Please install Redis manually.")
        logger.info("📖 Installation guide:")
        logger.info("   Ubuntu/Debian: sudo apt install redis-server")
        logger.info("   macOS: brew install redis")
        logger.info("   Windows: Download from https://redis.io/download")
        return False

def install_requirements():
    """Install Python requirements"""
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        logger.error("❌ requirements.txt not found")
        return False
    
    pip_cmd = get_pip_command()
    if not pip_cmd:
        logger.error("❌ Cannot find pip command")
        return False
    
    try:
        logger.info("📦 Installing Python dependencies...")
        result = subprocess.run(
            pip_cmd + ["install", "-r", requirements_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            logger.info("✅ Dependencies installed successfully")
            return True
        else:
            logger.error("❌ Failed to install requirements:")
            logger.error("STDOUT: %s", result.stdout)
            logger.error("STDERR: %s", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Installation timed out")
        return False
    except Exception as e:
        logger.error("❌ Failed to install requirements: %s", e)
        return False

def check_requirements():
    """Check if all requirements are installed"""
    required_modules = [
        'telegram',
        'sqlalchemy', 
        'redis',
        'gspread',
        'celery',
        'flask',
        'dotenv',
        'PIL',  # Pillow
        'qrcode',
        'requests',
        'captcha'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        logger.warning("⚠️  Missing modules: %s", ', '.join(missing_modules))
        return False
    
    logger.info("✅ All required modules are installed")
    return True

def setup_environment():
    """Setup the environment"""
    # Create necessary directories
    directories = ["logs", "assets", "assets/captcha_images", "data"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Check .env file
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            logger.warning("⚠️  .env file not found. Creating from template...")
            import shutil
            shutil.copy(".env.example", ".env")
            logger.info("✅ Created .env file from template")
            logger.warning("🔧 Please edit .env file with your actual values before running the bot")
            return False
        else:
            logger.error("❌ .env.example file not found. Cannot create .env file")
            return False
    
    logger.info("✅ Environment setup complete")
    return True

def validate_config():
    """Validate configuration"""
    try:
        # Try to import config module
        import importlib.util
        config_path = "config.py"
        if os.path.exists(config_path):
            spec = importlib.util.spec_from_file_location("config", config_path)
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)
            
            if hasattr(config, 'validate_config'):
                return config.validate_config()
            else:
                logger.info("✅ Config module loaded (no validation function)")
                return True
        else:
            logger.warning("⚠️  config.py not found, using default configuration")
            return True
    except ImportError:
        logger.error("❌ Cannot import config module")
        return False
    except Exception as e:
        logger.error("❌ Configuration validation failed: %s", e)
        return False

def create_dummy_assets():
    """Create dummy assets if they don't exist"""
    assets_script = "assets/create_dummy_images.py"
    if os.path.exists(assets_script):
        try:
            logger.info("🎨 Creating dummy assets...")
            subprocess.check_call([sys.executable, assets_script])
            logger.info("✅ Dummy assets created")
        except subprocess.CalledProcessError:
            logger.warning("⚠️  Could not create dummy assets (PIL might not be installed)")
        except Exception as e:
            logger.warning("⚠️  Error creating dummy assets: %s", e)

def test_captcha():
    """Test CAPTCHA functionality"""
    try:
        logger.info("🧪 Testing CAPTCHA functionality...")
        from PIL import Image, ImageDraw, ImageFont
        import random
        import string
        
        # Create a simple test CAPTCHA
        width, height = 200, 80
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Generate random text
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        
        # Try to draw text (with fallback if font not available)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 25), text, fill='black', font=font)
        
        # Save test image
        test_path = "assets/captcha_images/test_captcha.png"
        image.save(test_path)
        
        logger.info("✅ CAPTCHA test successful - saved to %s", test_path)
        return True
        
    except ImportError as e:
        logger.error("❌ CAPTCHA test failed - missing module: %s", e)
        return False
    except Exception as e:
        logger.error("❌ CAPTCHA test failed: %s", e)
        return False

def main():
    """Main function to run the bot"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment
    check_virtual_env()
    
    # Check and install requirements
    if not check_requirements():
        logger.info("📦 Installing missing dependencies...")
        if not install_requirements():
            logger.error("❌ Failed to install dependencies.")
            logger.info("💡 Try running manually:")
            logger.info("   python -m pip install -r requirements.txt")
            logger.info("   or")
            logger.info("   pip install -r requirements.txt")
            sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        logger.error("❌ Environment setup failed. Please check your .env configuration")
        sys.exit(1)
    
    # Validate configuration
    if not validate_config():
        logger.error("❌ Configuration validation failed. Please check your .env file")
        sys.exit(1)
    
    # Test CAPTCHA functionality
    test_captcha()
    
    # Check Redis (optional but recommended)
    if not check_redis():
        logger.info("🔄 Trying to start Redis...")
        if not start_redis():
            logger.warning("⚠️  Redis is not available. Some features may not work optimally.")
            logger.info("💡 The bot will use fallback mechanisms for caching and rate limiting")
    
    # Create dummy assets
    create_dummy_assets()
    
    # Start the bot
    logger.info("🤖 Starting JHOOM Airdrop Bot...")
    logger.info("🔗 Bot will be available once started")
    logger.info("📊 Admin panel: /admin")
    logger.info("🛑 Press Ctrl+C to stop the bot")
    
    try:
        # Import and run the bot
        from bot import main as bot_main
        bot_main()
    except KeyboardInterrupt:
        logger.info("\n👋 Bot stopped by user")
        logger.info("💾 All data has been saved")
    except ImportError as e:
        logger.error("❌ Import error: %s", e)
        logger.error("🔧 Please ensure all dependencies are installed")
        logger.info("💡 Try running the installation again")
        sys.exit(1)
    except Exception as e:
        logger.error("❌ Bot error: %s", e)
        logger.error("🔧 Please check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()