from app.utils.retry_connection import retry_connection
from app.utils.exception_handler import exception_handler
from app.utils.telegram_utils import send_telegram
from app.utils.logs_utils import write_log


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
    write_log(msg)
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
