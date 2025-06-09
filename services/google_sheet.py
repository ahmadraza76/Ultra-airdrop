import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_KEY, CREDENTIALS_FILE
from celery import shared_task

def init_google_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_KEY).sheet1

@shared_task
def save_user_async(telegram_id, wallet, points, joined_at):
    try:
        sheet = init_google_sheets()
        sheet.append_row([telegram_id, wallet, points, joined_at.isoformat()])
    except Exception as e:
        print(f"Google Sheets error: {e}")

@shared_task
def save_withdrawal_async(telegram_id, wallet, amount, requested_at):
    try:
        sheet = init_google_sheets()
        sheet.append_row([telegram_id, wallet, amount, requested_at.isoformat(), "Pending", ""])
    except Exception as e:
        print(f"Google Sheets error: {e}")

def save_user(telegram_id, wallet, points, joined_at):
    save_user_async.delay(telegram_id, wallet, points, joined_at)

def save_withdrawal(telegram_id, wallet, amount, requested_at):
    save_withdrawal_async.delay(telegram_id, wallet, amount, requested_at)
