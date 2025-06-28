import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_KEY, CREDENTIALS_FILE
from celery import shared_task
import os
import logging

logger = logging.getLogger(__name__)

def init_google_sheets():
    """Initialize Google Sheets connection"""
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            logger.warning(f"Credentials file {CREDENTIALS_FILE} not found")
            return None
            
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        
        if not GOOGLE_SHEET_KEY:
            logger.warning("GOOGLE_SHEET_KEY not configured")
            return None
            
        return client.open_by_key(GOOGLE_SHEET_KEY).sheet1
    except Exception as e:
        logger.error(f"Google Sheets initialization error: {e}")
        return None

@shared_task
def save_user_async(telegram_id, wallet, points, joined_at):
    """Async task to save user to Google Sheets"""
    try:
        sheet = init_google_sheets()
        if sheet:
            sheet.append_row([telegram_id, wallet, points, joined_at])
            logger.info(f"User {telegram_id} saved to Google Sheets")
    except Exception as e:
        logger.error(f"Google Sheets save user error: {e}")

@shared_task
def save_withdrawal_async(telegram_id, wallet, amount, requested_at):
    """Async task to save withdrawal to Google Sheets"""
    try:
        sheet = init_google_sheets()
        if sheet:
            sheet.append_row([telegram_id, wallet, amount, requested_at, "Pending", ""])
            logger.info(f"Withdrawal for {telegram_id} saved to Google Sheets")
    except Exception as e:
        logger.error(f"Google Sheets save withdrawal error: {e}")

def save_user(telegram_id, wallet, points, joined_at):
    """Queue user save task"""
    try:
        save_user_async.delay(telegram_id, wallet, points, joined_at.isoformat())
    except Exception as e:
        logger.error(f"Error queuing user save task: {e}")

def save_withdrawal(telegram_id, wallet, amount, requested_at):
    """Queue withdrawal save task"""
    try:
        save_withdrawal_async.delay(telegram_id, wallet, amount, requested_at.isoformat())
    except Exception as e:
        logger.error(f"Error queuing withdrawal save task: {e}")