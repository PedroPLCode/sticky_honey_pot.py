import os
from datetime import datetime as dt
from utils.retry_connection import retry_connection
from utils.exception_handler import exception_handler
from app.utils.telegram_utils import send_telegram
from config import LOG_DIR


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
    save_log(msg)
    send_telegram(msg)
    
    
@exception_handler()
def create_alert_log_msg(
    timestamp: str,
    ip: str,
    port: int | str,
    service: str,
    data: str,
    geo: dict[str, str],
    threats: list[str] | None = None,
):
    """
    Generates a formatted honeypot alert log message with details about a detected event.
    Args:
        timestamp (str): The timestamp of the alert event.
        ip (str): The IP address involved in the alert.
        port (int or str): The port number associated with the alert.
        service (str): The service running on the specified port.
        data (str): The data or payload associated with the alert.
        geo (dict): Geolocation information containing 'country', 'city', and 'isp'.
        threats (list of str, optional): List of detected threats related to the event.
    Returns:
        str: A formatted alert log message containing all provided details.
    """
    alert_log_msg = (
        f"!!! HONEYPOT ALERT !!!\n"
        f"Timestamp: {timestamp}\n"
        f"IP: {ip} Port: {port} ({service})\n"
        f"Data: `{data}`\n"
        f"Location: {geo['country']}, {geo['city']} ({geo['isp']})"
    )
    if threats:
        alert_log_msg += f"Threats: {', '.join(threats)}\n"

    return alert_log_msg


@exception_handler()
def save_log(log_msg: str):
    """
    Saves a log message to a daily log file and prints it to the console.

    The log file is created in the directory specified by LOG_DIR, with the filename
    formatted as 'honeypot_log_<YYYY-MM-DD>.txt'. Each log entry is prepended with a
    timestamp in the format 'YYYY-MM-DD HH:MM:SS'.

    Args:
        log_msg (str): The message to be logged.

    Raises:
        OSError: If the log directory cannot be created or the log file cannot be written.
    """
    log_dir = LOG_DIR
    os.makedirs(log_dir, exist_ok=True)

    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = timestamp.split(" ")[0]
    log_file = os.path.join(log_dir, f"honeypot_log_{date_str}.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {log_msg}\n")

    print(f"[{timestamp}] {log_msg}\n")
