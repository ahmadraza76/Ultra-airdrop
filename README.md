#Altra Airdrop Bot
A hybrid Telegram bot for managing airdrop campaigns with an off-chain points system, manual withdrawals, guided onboarding, and comprehensive documentation.
Setup

Install dependencies:
pip install -r requirements.txt


Configure .env (see .env template).

Place images in assets/ and CAPTCHA images in assets/captcha_images/.

Set up Google Sheets:

Create a sheet with columns: Telegram ID, Wallet, Amount, Requested At, Status, Processed At.
Share with service account email from credentials.json.


Set up Google Apps Script:

Open Google Sheet → Extensions → Apps Script.
Paste notify.js and replace YOUR_NOTIFY_BOT_TOKEN.
Add a trigger: Edit → Current project's triggers → Add Trigger → onEdit → From spreadsheet → On edit.


Set up CAPTCHA web server:

Create a Flask/Django server for BASE_URL/captcha/{user_id}/{code}.
Verify code in Redis and serve CAPTCHA image.


Run locally:
python bot.py


Deploy with Docker:
docker-compose up -d



Features

Guided Onboarding: Step-by-step setup (CAPTCHA, wallet, tasks, referrals).
Help Center: /help with detailed instructions.
FAQ: Accessible via menu.
Video Guides: Task tutorials via YouTube links.
Inline CAPTCHA: Private chat links with 2-minute validity.
Off-Chain Points: JHOOM Points for tasks, shown via /balance.
Manual Withdrawals: Requests saved to Google Sheets; admins process and notify.
Admin Controls: Stats, broadcast, pause, export, logs.

Withdrawal Process

User requests withdrawal (min 100 points).
Bot saves to SQLite and Google Sheets.
Admin sends tokens via MetaMask/TrustWallet.
Admin marks Status as "Paid" in Google Sheet.
Google Apps Script notifies user via Telegram.

Testing
Run tests:
pytest

Notes

Replace video guide URLs in config.py.
Implement CAPTCHA web server for BASE_URL/captcha.
Secure .env and credentials.json in production.

