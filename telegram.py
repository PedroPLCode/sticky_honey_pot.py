import asyncio
from telegram import Bot as TelegramBot
from retry_connection import retry_connection
from exception_handler import exception_handler
from logger import save_log
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

@exception_handler()
@retry_connection()
def init_telegram_bot() -> TelegramBot:
    return TelegramBot(token=TELEGRAM_BOT_TOKEN)


@exception_handler(default_return=False)
@retry_connection()
def send_telegram(msg: str) -> bool:
    telegram_bot = init_telegram_bot()

    if telegram_bot:
        asyncio.run(telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg))
        log_msg = f"Telegram {TELEGRAM_CHAT_ID} {msg} sent succesfully."
        save_log(log_msg)
        return True

    return False