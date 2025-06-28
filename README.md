# 🚀 JHOOM Airdrop Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-20.7-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**A Professional Telegram Airdrop Bot with Advanced Features**

*Developed by [Your Name] - Professional Bot Developer*

[🔗 Live Demo](#) • [📖 Documentation](#features) • [🚀 Quick Start](#quick-start) • [💬 Support](#support)

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Installation](#️-installation)
- [🔧 Configuration](#-configuration)
- [🏃‍♂️ Running the Bot](#️-running-the-bot)
- [🌐 Deployment](#-deployment)
- [📊 Admin Panel](#-admin-panel)
- [🔒 Security](#-security)
- [🧪 Testing](#-testing)
- [❓ FAQ](#-faq)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

### 🎯 Core Features
- **🔐 Advanced CAPTCHA System** - Secure user verification with image-based CAPTCHAs
- **💰 Points-Based Rewards** - JHOOM Points system for task completion
- **📱 Guided Onboarding** - Step-by-step user registration process
- **🎁 Referral System** - Earn points by inviting friends
- **📋 Task Management** - Automated task verification and rewards
- **💸 Withdrawal System** - Secure token distribution via Google Sheets
- **👨‍💼 Admin Dashboard** - Complete bot management interface

### 🛡️ Security Features
- **🔒 Rate Limiting** - Prevents spam and abuse
- **✅ Wallet Validation** - BEP-20/ERC-20 address verification
- **🔐 Redis Caching** - Secure session management
- **📊 Activity Logging** - Complete audit trail
- **🚫 Anti-Bot Protection** - Multiple verification layers

### 🎨 User Experience
- **📚 Interactive Help Center** - Comprehensive user guidance
- **🎥 Video Tutorials** - YouTube integration for task guides
- **❓ FAQ System** - Built-in frequently asked questions
- **🌟 Rich Media Support** - Images, banners, and icons
- **📱 Mobile Optimized** - Perfect Telegram experience

---

## 🚀 Quick Start

### Prerequisites
- 🐍 Python 3.11+
- 🔴 Redis Server
- 📊 Google Sheets API Access
- 🤖 Telegram Bot Token

### One-Line Setup
```bash
git clone <repository> && cd jhoom-airdrop-bot && chmod +x start.sh && ./start.sh
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone <your-repository-url>
cd jhoom-airdrop-bot
```

### 2️⃣ Install Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using the setup script
python setup.py
```

### 3️⃣ Create Environment
```bash
# Copy environment template
cp .env.example .env

# Edit with your values
nano .env
```

---

## 🔧 Configuration

### 📝 Environment Variables (.env)
```env
# 🤖 Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
NOTIFY_BOT_TOKEN=your_notification_bot_token_here

# 👨‍💼 Admin Configuration  
ADMIN_IDS=123456789,987654321

# 📢 Telegram Channels/Groups
TELEGRAM_CHANNEL=@your_channel
TELEGRAM_GROUP=@your_group

# 📊 Google Sheets Integration
GOOGLE_SHEET_KEY=your_google_sheet_key_here
CREDENTIALS_FILE=credentials.json

# 🔴 Redis Configuration
REDIS_URL=redis://localhost:6379/0

# ⚡ Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# 🌐 Web Server Configuration
BASE_URL=https://your-domain.com
PORT=8000
```

### 📊 Google Sheets Setup

1. **Create Google Sheet** with columns:
   ```
   Telegram ID | Wallet | Amount | Requested At | Status | Processed At
   ```

2. **Service Account Setup**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable Google Sheets API
   - Create Service Account
   - Download `credentials.json`

3. **Share Sheet** with service account email

### 🔔 Google Apps Script (Auto-Notifications)
```javascript
function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  var range = e.range;
  var row = range.getRow();
  var column = range.getColumn();

  if (sheet.getName() === "Sheet1" && column === 5 && range.getValue() === "Paid") {
    var telegramId = sheet.getValue(row, 1);
    var wallet = sheet.getValue(row, 2);
    var amount = sheet.getValue(row, 3);
    var processedAt = sheet.getValue(row, 6);

    var message = `🎉 *Withdrawal Processed*\n\n` +
                  `Wallet: ${wallet}\n` +
                  `Amount: ${amount} JHOOM Points\n` +
                  `Processed: ${processedAt}\n\n` +
                  `Thank you for participating in the JHOOM Airdrop!`;

    var url = `https://api.telegram.org/bot${YOUR_NOTIFY_BOT_TOKEN}/sendMessage`;
    var payload = {
      chat_id: telegramId,
      text: message,
      parse_mode: "Markdown"
    };

    UrlFetchApp.fetch(url, {
      method: "POST",
      contentType: "application/json",
      payload: JSON.stringify(payload)
    });
  }
}
```

---

## 🏃‍♂️ Running the Bot

### 🖥️ Local Development
```bash
# Start Redis
redis-server

# Start the bot
python run_bot.py

# Or using npm scripts
npm run dev
```

### 🐳 Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f bot
```

### ⚡ Background Services
```bash
# Start Celery worker (for background tasks)
celery -A bot.celery worker --loglevel=info

# Start CAPTCHA web server
python captcha_server.py
```

---

## 🌐 Deployment

### 🚂 Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway up
```

### 🟣 Heroku
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set BOT_TOKEN=your_token

# Deploy
git push heroku main
```

### ☁️ VPS/Cloud Server
```bash
# Clone repository
git clone <repository>
cd jhoom-airdrop-bot

# Install dependencies
pip install -r requirements.txt

# Start with PM2 (recommended)
pm2 start ecosystem.config.js
```

### 📋 Supported Platforms

| Platform | Method | Files Required | Notes |
|----------|--------|----------------|-------|
| 🚂 Railway | `railway.yml` | `Dockerfile`, `railway.yml` | Best for CI/CD |
| 🟣 Heroku | `Procfile` | `Procfile`, `requirements.txt` | Free tier available |
| 🔄 Replit | Nix Config | `replit.nix`, `.replit` | Easy setup |
| 🐳 VPS | Docker | `docker-compose.yml` | Full control |
| ⚡ Render | Auto-deploy | `render.yaml` | Similar to Railway |
| 🌐 Fly.io | `fly.toml` | `fly.toml`, `Dockerfile` | Fast deployment |

---

## 📊 Admin Panel

### 🔑 Admin Commands
- `/admin` - Access admin panel
- `/start` - Regular user start command

### 📈 Admin Features
- **📊 Statistics Dashboard** - User count, points, withdrawals
- **📢 Broadcast Messages** - Send announcements to all users
- **⏸️ Pause/Resume Bot** - Emergency controls
- **📤 Export Users** - Download user data as Excel
- **📜 Activity Logs** - View recent user actions
- **💸 Withdrawal Management** - Process token distributions

### 📊 Analytics & Monitoring
```python
# View bot statistics
Total Users: 1,234
Active Users: 987
Pending Withdrawals: 45
Total Points Distributed: 12,345
```

---

## 🔒 Security

### 🛡️ Security Features
- **🔐 Environment Variables** - Sensitive data protection
- **🚫 Rate Limiting** - Prevents abuse and spam
- **✅ Input Validation** - Wallet address verification
- **📊 Activity Logging** - Complete audit trail
- **🔒 Redis Security** - Secure session management

### 🔐 Best Practices
```bash
# Secure file permissions
chmod 600 .env
chmod 600 credentials.json

# Use strong passwords
# Enable 2FA on all accounts
# Regular security updates
```

---

## 🧪 Testing

### 🔬 Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run specific test file
pytest tests/test_captcha.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### 🧪 Test Coverage
- ✅ CAPTCHA Generation & Verification
- ✅ Wallet Validation
- ✅ User Registration Flow
- ✅ Task Completion
- ✅ Withdrawal Process
- ✅ Admin Functions

---

## ❓ FAQ

<details>
<summary><strong>🤔 How do I get a Telegram Bot Token?</strong></summary>

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided
</details>

<details>
<summary><strong>📊 How do I set up Google Sheets integration?</strong></summary>

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API
4. Create a Service Account
5. Download the JSON credentials file
6. Share your Google Sheet with the service account email
</details>

<details>
<summary><strong>🔴 Why do I need Redis?</strong></summary>

Redis is used for:
- CAPTCHA code storage
- Rate limiting
- Session management
- Background task queuing
</details>

<details>
<summary><strong>💰 How does the withdrawal process work?</strong></summary>

1. User requests withdrawal (minimum 100 points)
2. Request is saved to database and Google Sheets
3. Admin manually sends tokens via wallet
4. Admin marks status as "Paid" in Google Sheets
5. User receives automatic notification
</details>

---

## 🛠️ Troubleshooting

### ❌ Common Issues

#### `ModuleNotFoundError: No module named 'telegram'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

#### `Redis connection failed`
```bash
# Solution: Start Redis server
redis-server

# Or install Redis
# Ubuntu/Debian: sudo apt install redis-server
# macOS: brew install redis
# Windows: Download from Redis website
```

#### `Google Sheets API error`
```bash
# Solution: Check credentials.json file
# Ensure service account has access to the sheet
# Verify GOOGLE_SHEET_KEY in .env file
```

#### `CAPTCHA images not loading`
```bash
# Solution: Create dummy images
python assets/create_dummy_images.py

# Or add your own images to assets/ folder
```

### 🔧 Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python run_bot.py
```

### 📞 Getting Help
- 📧 Email: support@yourproject.com
- 💬 Telegram: [@YourSupport](https://t.me/yoursupport)
- 🐛 Issues: [GitHub Issues](https://github.com/yourrepo/issues)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### 🔄 Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### 📝 Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Write tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Developed with ❤️ by [Your Name]**

- 🌐 Website: [yourwebsite.com](https://yourwebsite.com)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- 🐦 Twitter: [@YourTwitter](https://twitter.com/yourtwitter)
- 📧 Email: your.email@domain.com

### 🏆 Expertise
- 🤖 Telegram Bot Development
- 🐍 Python Backend Development
- 📊 Database Design & Optimization
- 🔒 Security & Authentication
- ☁️ Cloud Deployment & DevOps

---

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Google Sheets API](https://developers.google.com/sheets/api) - Spreadsheet integration
- [Redis](https://redis.io/) - In-memory data structure store
- [Celery](https://celeryproject.org/) - Distributed task queue

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Made with ❤️ for the crypto community

[🔝 Back to Top](#-jhoom-airdrop-bot)

</div>