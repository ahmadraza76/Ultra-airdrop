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

# Check if Python 3.11+ is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)'; then
            print_status "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.11+ required. Found: $PYTHON_VERSION"
            exit 1
        fi
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)'; then
            print_status "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
        else
            print_error "Python 3.11+ required. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python not found. Please install Python 3.11+"
        exit 1
    fi
}

# Create virtual environment if it doesn't exist
setup_venv() {
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_status "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi

    # Activate virtual environment
    print_info "Activating virtual environment..."
    source venv/bin/activate
    print_status "Virtual environment activated"
}

# Install requirements
install_requirements() {
    print_info "Installing Python dependencies..."
    if pip install -r requirements.txt; then
        print_status "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        exit 1
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
            print_error ".env.example not found"
            exit 1
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
            print_warning "Could not create dummy assets (PIL might not be installed)"
        fi
    fi
}

# Check Redis
check_redis() {
    if command -v redis-server &> /dev/null; then
        print_info "Starting Redis server..."
        if redis-server --daemonize yes; then
            print_status "Redis server started"
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
    check_redis

    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📝 Next steps:"
    echo "1. Edit .env file with your bot tokens and configuration"
    echo "2. Replace credentials.json with your Google Service Account credentials"
    echo "3. Replace dummy images in assets/ with your actual images"
    echo "4. Run the bot: $PYTHON_CMD run_bot.py"
    echo ""
    echo "📖 For detailed instructions, see README.md"
    echo "💬 For support, contact: [your-support-contact]"
    echo ""
    print_status "Ready to launch! 🚀"
}

# Run main function
main