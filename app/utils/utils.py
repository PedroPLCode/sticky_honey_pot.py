from utils.retry_connection import retry_connection
from utils.exception_handler import exception_handler

@exception_handler(default_return=False)
@retry_connection()
def save_log_and_send_telegram(msg: str):
    """
    Saves a log message and sends it via Telegram.
    This function first saves the provided message to the log using `save_log`,
    then sends the same message as a Telegram notification using `send_telegram`.
    It is decorated to automatically retry the connection on failure and to handle
    exceptions gracefully, returning False if an exception occurs.
    Args:
        msg (str): The message to be logged and sent.
    Returns:
        bool: True if both operations succeed, False otherwise.
    """
    from utils.logger import save_log
    save_log(msg)
    
    from utils.telegram_notify import send_telegram
    send_telegram(msg)