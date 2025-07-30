from retry_connection import retry_connection
from exception_handler import exception_handler

@exception_handler(default_return=False)
@retry_connection()
def save_log_and_send_telegram(msg):
    from logger import save_log
    save_log(msg)
    
    from telegram_notify import send_telegram
    send_telegram(msg)