from telegram import Bot
from retry_connection import retry_connection
from exception_handler import exception_handler
from logger import save_log
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import asyncio
import traceback

@exception_handler()
@retry_connection()
def send_telegram(msg: str) -> bool:
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        async def send():
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
        
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        
        if loop and loop.is_running():
            asyncio.create_task(send())
        else:
            asyncio.run(send())

        save_log(f"Telegram {TELEGRAM_CHAT_ID} - {msg} - sent successfully.")
        return True

    except Exception as e:
        tb = traceback.format_exc()
        save_log(f"[Telegram] Sending failed: {e}\n{tb}")
        return False