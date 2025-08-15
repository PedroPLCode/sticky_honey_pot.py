import asyncio
import traceback
from telegram import Bot
from utils.retry_connection import retry_connection
from utils.exception_handler import exception_handler
from utils.logger import save_log
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


@exception_handler()
@retry_connection()
def send_telegram(msg: str) -> bool:
    """
    Sends a message to a specified Telegram chat using a bot.
    This function attempts to send the provided message to the Telegram chat identified by `TELEGRAM_CHAT_ID`
    using the bot token `TELEGRAM_BOT_TOKEN`. It handles both running and non-running asyncio event loops,
    ensuring compatibility in synchronous and asynchronous contexts. The function logs the result of the operation.
    Args:
        msg (str): The message to send to the Telegram chat.
    Returns:
        bool: True if the message was sent successfully, False otherwise.
    Logs:
        - Success or failure of the message sending operation, including exception tracebacks on failure.
    """
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

        save_log(f"Telegram {TELEGRAM_CHAT_ID} sent successfully.")
        return True

    except Exception as e:
        tb = traceback.format_exc()
        save_log(f"[Telegram] Sending failed: {e}\n{tb}")
        return False
