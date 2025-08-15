from utils.retry_connection import retry_connection
from utils.exception_handler import exception_handler


@exception_handler(default_return=False)
@retry_connection()
def save_log_and_send_telegram(msg: str):
    """
    Logs a message and sends it via Telegram notification.
    This function first saves the provided message to the log using the `save_log` function,
    and then sends the same message as a Telegram notification using the `send_telegram` function.
    Args:
        msg (str): The message to be logged and sent via Telegram.
    """
    from logger import save_log
    save_log(msg)

    from telegram_notify import send_telegram
    send_telegram(msg)
