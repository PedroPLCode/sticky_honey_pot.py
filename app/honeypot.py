"""
A multi-threaded honeypot server that listens on specified ports, emulates various services, and logs suspicious activity.
For each incoming connection, the honeypot sends a service-specific banner, receives data, detects potential exploits,
Modules:
    - socket: For network communication.
    - threading: For handling multiple connections concurrently.
    - datetime: For timestamping events.
    - app.utils.exception_handler: Decorator for exception handling.
    - app.utils.alert_logs_utils: For creating log messages.
    - app.utils.geoip: For GeoIP lookups.
    - app.utils.telegram_utils: For logging and sending Telegram alerts.
    - app.utils.exploit_detector: For exploit detection.
    - app.config: Contains service banners and port mappings.
Functions:
    - handle_client(client_socket, ip, port, service): Handles a single client connection, processes data, detects threats, logs, and alerts.
    - start_server(port, service): Starts a honeypot server on a given port and service, spawning threads for each connection.
Execution:
    When run as the main module, starts honeypot servers for all configured ports/services and handles graceful shutdown on KeyboardInterrupt.
"""

import socket
import threading
from datetime import datetime as dt
from app.utils.exception_handler import exception_handler
from app.utils.alert_utils import create_alert_log_msg
from app.utils.geoip_lookup import geoip_lookup
from app.utils.alert_utils import save_log_and_send_telegram
from app.utils.exploit_detector import detect_exploit
from app.config import BANNER, PORTS


def handle_client(client_socket: socket.socket, ip: str, port: int, service: str):
    """
    Handles an incoming client connection to the honeypot.
    Sends a service-specific banner to the client, receives data, detects potential exploits,
    performs GeoIP lookup, logs the event, and sends alerts via Telegram.
    Args:
        client_socket (socket.socket): The socket object representing the client connection.
        ip (str): The IP address of the client.
        port (int): The port number on which the client connected.
        service (str): The name of the service being emulated.
    Exceptions:
        Logs and sends any exceptions encountered during handling.
    Returns:
        None
    """
    try:
        banner = BANNER.get(service, "Hello.\n")

        client_socket.send(banner.encode())
        data = client_socket.recv(1024).decode("utf-8", errors="ignore")

        threats = detect_exploit(data)
        geo = geoip_lookup(ip)
        timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")

        log_msg = create_alert_log_msg(timestamp, ip, port, service, data, geo, threats)
        save_log_and_send_telegram(log_msg)

    except Exception as e:
        error_msg = f"[!] Error: {e}"
        save_log_and_send_telegram(error_msg)
    finally:
        client_socket.close()


@exception_handler()
def start_server(port: int, service: str):
    """
    Starts a honeypot server that listens for incoming TCP connections on the specified port and service.

    Args:
        port (int): The port number on which the server will listen for connections.
        service (str): The name of the service to emulate (for logging and identification).

    Side Effects:
        - Binds a socket to all network interfaces on the given port.
        - Logs a startup message and sends it via Telegram.
        - For each incoming connection, spawns a new thread to handle the client.

    Note:
        The function runs indefinitely, accepting and handling connections in separate threads.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    start_msg = f"Honeypot listening on port {port} as {service}"
    save_log_and_send_telegram(start_msg)

    while True:
        client_socket, addr = server.accept()
        ip = addr[0]
        thread = threading.Thread(
            target=handle_client, args=(client_socket, ip, port, service)
        )
        thread.start()


if __name__ == "__main__":
    try:
        for port, service in PORTS.items():
            t = threading.Thread(target=start_server, args=(port, service), daemon=True)
            t.start()
        while True:
            pass
    except KeyboardInterrupt:
        shutdown_msg = "Honeypot shutting down."
        save_log_and_send_telegram(shutdown_msg)
