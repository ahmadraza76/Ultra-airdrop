#!/bin/bash

# 🚀 JHOOM Airdrop Bot - Professional Setup Script
# Developed by [Your Name] - Professional Bot Developer

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🚀 JHOOM AIRDROP BOT 🚀                   ║"
echo "║                                                              ║"
echo "║              Professional Setup & Installation              ║"
echo "║                                                              ║"
echo "║              Developed by [Your Name]                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to find working Python command
find_python() {
    for cmd in python3 python; do
        if command -v $cmd &> /dev/null; then
            if $cmd -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)' 2>/dev/null; then
                echo $cmd
                return 0
            fi
        fi
    done
    return 1
}

# Function to find working pip command
find_pip() {
    local python_cmd=$1
    
    # Try different pip approaches
    if $python_cmd -m pip --version &> /dev/null; then
        echo "$python_cmd -m pip"
        return 0
    elif command -v pip3 &> /dev/null; then
        echo "pip3"
        return 0
    elif command -v pip &> /dev/null; then
        echo "pip"
        return 0
    fi
    return 1
}

# Check if Python 3.8+ is installed
check_python() {
    PYTHON_CMD=$(find_python)
    if [ $? -eq 0 ]; then
        PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_status "Python $PYTHON_VERSION found ($PYTHON_CMD)"
    else
        print_error "Python 3.8+ not found. Please install Python 3.8+"
        exit 1
    fi
}

# Create virtual environment if it doesn't exist
setup_venv() {
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        if $PYTHON_CMD -m venv venv; then
            print_status "Virtual environment created"
        else
            print_error "Failed to create virtual environment"
            exit 1
        fi
    else
        print_status "Virtual environment already exists"
    fi

    # Activate virtual environment
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_status "Virtual environment activated"
    
    # Update PYTHON_CMD to use venv python
    PYTHON_CMD="python"
}

# Install requirements
install_requirements() {
    print_info "Finding pip command..."
    PIP_CMD=$(find_pip $PYTHON_CMD)
    if [ $? -ne 0 ]; then
        print_error "No working pip command found"
        print_info "Trying to install pip..."
        if $PYTHON_CMD -m ensurepip --upgrade; then
            PIP_CMD="$PYTHON_CMD -m pip"
            print_status "pip installed successfully"
        else
            print_error "Failed to install pip"
            exit 1
        fi
    else
        print_status "Using pip: $PIP_CMD"
    fi

    print_info "Upgrading pip..."
    $PIP_CMD install --upgrade pip

    print_info "Installing Python dependencies..."
    if $PIP_CMD install -r requirements.txt; then
        print_status "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        print_info "Trying alternative installation method..."
        if $PIP_CMD install --user -r requirements.txt; then
            print_status "Dependencies installed with --user flag"
        else
            print_error "All installation methods failed"
            exit 1
        fi
    fi
}

# Create necessary directories
create_directories() {
    print_info "Creating necessary directories..."
    mkdir -p logs assets assets/captcha_images data
    print_status "Directories created"
}

# Setup environment file
setup_env() {
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_status "Created .env file from template"
            print_warning "Please edit .env file with your actual values"
        else
            print_warning ".env.example not found, creating basic .env template"
            cat > .env << 'EOF'
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_id_here

# Database Configuration
DATABASE_URL=sqlite:///data/bot.db

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0

# Google Sheets Configuration (optional)
GOOGLE_SHEETS_ENABLED=false
GOOGLE_SHEET_ID=your_sheet_id_here

# Bot Configuration
MAX_USERS=10000
CAPTCHA_ENABLED=true
RATE_LIMIT_ENABLED=true
EOF
            print_status "Created basic .env template"
            print_warning "Please edit .env file with your actual values"
        fi
    else
        print_status ".env file already exists"
    fi
}

# Create credentials template
setup_credentials() {
    if [ ! -f "credentials.json" ]; then
        print_info "Creating credentials.json template..."
        cat > credentials.json << 'EOF'
{
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
EOF
        print_status "Created credentials.json template"
        print_warning "Please replace with your actual Google Service Account credentials"
    else
        print_status "credentials.json already exists"
    fi
}

# Create dummy assets
create_assets() {
    if [ -f "assets/create_dummy_images.py" ]; then
        print_info "Creating dummy assets..."
        if $PYTHON_CMD assets/create_dummy_images.py; then
            print_status "Dummy assets created"
        else
            print_warning "Could not create dummy assets"
        fi
    fi
}

# Test CAPTCHA functionality
test_captcha() {
    print_info "Testing CAPTCHA functionality..."
    if $PYTHON_CMD -c "
from PIL import Image, ImageDraw, ImageFont
import random, string, os
os.makedirs('assets/captcha_images', exist_ok=True)
img = Image.new('RGB', (200, 80), 'white')
draw = ImageDraw.Draw(img)
text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
try:
    font = ImageFont.truetype('arial.ttf', 36)
except:
    font = ImageFont.load_default()
draw.text((50, 25), text, fill='black', font=font)
img.save('assets/captcha_images/test_captcha.png')
print('CAPTCHA test successful')
" 2>/dev/null; then
        print_status "CAPTCHA functionality working"
    else
        print_warning "CAPTCHA test failed, but dependencies should be installed"
    fi
}

# Check Redis
check_redis() {
    if command -v redis-server &> /dev/null; then
        print_info "Starting Redis server..."
        if redis-server --daemonize yes 2>/dev/null; then
            sleep 2
            if redis-cli ping &> /dev/null; then
                print_status "Redis server started and running"
            else
                print_warning "Redis server started but not responding"
            fi
        else
            print_warning "Could not start Redis server"
        fi
    else
        print_warning "Redis not found. Please install Redis for full functionality:"
        print_info "  Ubuntu/Debian: sudo apt install redis-server"
        print_info "  macOS: brew install redis"
        print_info "  Windows: Download from https://redis.io/download"
    fi
}

# Main setup process
main() {
    echo "🚀 Starting JHOOM Airdrop Bot setup..."
    echo ""

    check_python
    setup_venv
    install_requirements
    create_directories
    setup_env
    setup_credentials
    create_assets
    test_captcha
    check_redis

    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📝 Next steps:"
    echo "1. Edit .env file with your bot tokens and configuration"
    echo "2. Replace credentials.json with your Google Service Account credentials (if using Google Sheets)"
    echo "3. Replace dummy images in assets/ with your actual images"
    echo "4. Run the bot: $PYTHON_CMD run_bot.py"
    echo ""
    echo "🔧 Quick start:"
    echo "   source venv/bin/activate  # Activate virtual environment"
    echo "   $PYTHON_CMD run_bot.py    # Run the bot"
    echo ""
    echo "📖 For detailed instructions, see README.md"
    echo "💬 For support, contact: [your-support-contact]"
    echo ""
    print_status "Ready to launch! 🚀"
}

# Run main function
main