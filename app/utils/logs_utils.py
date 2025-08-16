import os
from datetime import datetime as dt
from utils.exception_handler import exception_handler
from config import LOG_DIR


@exception_handler()
def write_log(log_msg: str):
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
    