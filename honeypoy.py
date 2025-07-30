import socket
import threading
import datetime

from config import PORTS
from db import init_db, save_log
from geoip import geoip_lookup

from exploit_detector import detect_exploit, classify_threat
from telegram import send_telegram


def handle_client(client_socket, ip, port, service):
    try:
        banner = {
            "SSH": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n",
            "FTP": "220 (vsFTPd 3.0.3)\n",
            "HTTP": "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>It works!</h1></body></html>\n"
        }.get(service, "Hello.\n")

        client_socket.send(banner.encode())
        data = client_socket.recv(1024).decode("utf-8", errors="ignore")
        now = str(datetime.datetime.now())

        threats = detect_exploit(data)
        severity = classify_threat(threats) if threats else "None"
        geo = geoip_lookup(ip)
        save_log(now, ip, port, service, data, geo)
        send_telegram(ip, port, service, data, geo, threats, severity)

        print(f"[+] Logged: {ip} on port {port} ({service})")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()

def start_server(port, service):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[+] Honeypot listening on port {port} as {service}")

    while True:
        client_socket, addr = server.accept()
        ip = addr[0]
        thread = threading.Thread(target=handle_client, args=(client_socket, ip, port, service))
        thread.start()

if __name__ == "__main__":
    init_db()
    for port, service in PORTS.items():
        t = threading.Thread(target=start_server, args=(port, service))
        t.start()
