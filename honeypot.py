import socket
import threading
from datetime import datetime as dt
from exception_handler import exception_handler
from logger import create_alert_log_msg
from geoip import geoip_lookup
from utils import save_log_and_send_telegram
from exploit_detector import detect_exploit
from config import BANNER, PORTS

def handle_client(client_socket, ip, port, service):
    try:
        banner = BANNER.get(service, "Hello.\n")

        client_socket.send(banner.encode())
        data = client_socket.recv(1024).decode("utf-8", errors="ignore")

        threats = detect_exploit(data)
        geo = geoip_lookup(ip)
        timestamp=dt.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_msg = create_alert_log_msg(timestamp, ip, port, service, data, geo, threats)
        save_log_and_send_telegram(log_msg)

    except Exception as e:
        error_msg = f"[!] Error: {e}"
        save_log_and_send_telegram(error_msg)
    finally:
        client_socket.close()


@exception_handler()
def start_server(port, service):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    start_msg = f"Honeypot listening on port {port} as {service}"
    save_log_and_send_telegram(start_msg)

    while True:
        client_socket, addr = server.accept()
        ip = addr[0]
        thread = threading.Thread(target=handle_client, args=(client_socket, ip, port, service))
        thread.start()


if __name__ == "__main__":
    for port, service in PORTS.items():
        t = threading.Thread(target=start_server, args=(port, service))
        t.start()