import pytest
from telegram import Update, Message, Chat
from telegram.ext import Application
from handlers.start import start
from handlers.message import handle_message
from database.db import Session, init_db
from database.models import User

@pytest.mark.asyncio
async def test_user_flow():
    init_db()
    app = Application.builder().token("mock_token").build()
    update = Update(
        update_id=1,
        message=Message(
            message_id=1,
            chat=Chat(id=123, type="private"),
            text="/start",
        ),
    )
    context = app.create_context(update)
    
    await start(update, context)
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=123).first()
        assert user is not None
        assert context.user_data["state"] == "captcha"
    
    update.message.text = context.user_data["captcha"]
    await handle_message(update, context)
    assert context.user_data["state"] == "onboarding"
