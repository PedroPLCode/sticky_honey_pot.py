import os
import datetime
from exception_handler import exception_handler
from config import LOG_DIR

@exception_handler()
def create_alert_log_msg(timestamp, ip, port, service, data, geo, threats=None):
    alert_log_msg = (
        f"Honeypot Alert\n"
        f"Timestamp: {timestamp}\n"
        f"IP: {ip} Port: {port} ({service})\n"
        f"Data: `{data}`\n"
        f"Location: {geo['country']}, {geo['city']} ({geo['isp']})"
    )
    if threats:
        alert_log_msg += f"\nThreats: {', '.join(threats)}\n"
        
    return alert_log_msg


@exception_handler()
def save_log(log_msg):
    log_dir = LOG_DIR
    os.makedirs(log_dir, exist_ok=True)

    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = timestamp.split(" ")[0]
    log_file = os.path.join(log_dir, f"honeypot_log_{date_str}.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_msg)
        
    print(f"{log_msg}\n\nLog updated succesfully.")