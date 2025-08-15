"""
Configuration module for the honey pot application.

Loads environment variables using dotenv and defines constants for bot integration,
network service emulation, attack pattern detection, and logging.

Attributes:
    TELEGRAM_BOT_TOKEN (str): Telegram bot token loaded from environment.
    TELEGRAM_CHAT_ID (str): Telegram chat ID loaded from environment.
    IP_API_URL (str): URL for IP geolocation API.
    LOG_DIR (str): Directory for storing logs.
    PORTS (dict): Mapping of port numbers to service names (SSH, FTP, HTTP).
    BANNER (dict): Service banners for emulated protocols.
    SQL_ATTACK_PATTERNS (list): List of tuples containing regex patterns and attack type descriptions
        for detecting various security threats, including SQL Injection, XSS, LFI, RFI, Command Injection,
        Web Shells, SSTI, LDAP Injection, XXE, SSRF, and code execution/obfuscation.
"""
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

IP_API_URL = 'http://ip-api.com/json/'

LOG_DIR = 'logs'

PORTS = {
    2222: "SSH",
    2121: "FTP",
    8080: "HTTP"
}

BANNER = {
    "SSH": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n",
     "FTP": "220 (vsFTPd 3.0.3)\n",
    "HTTP": "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>It works!</h1></body></html>\n"
}

SQL_ATTACK_PATTERNS = [
    # SQL Injection
    (r"(?i)(\bunion\b|\bselect\b.*\bfrom\b|\binformation_schema\b|\bor\s+\d=\d|\b'--|\b\"--)", "SQL Injection"),
    (r"(?i)(\bxp_cmdshell\b|\bsleep\(\d+\)|benchmark\(\d+,)", "Time-Based SQLi"),

    # XSS
    (r"(?i)<script.*?>.*?</script.*?>", "XSS (Script Tag)"),
    (r"(?i)(onerror|onload|alert\()", "XSS (Event Handler)"),
    (r"(?i)(<iframe|<img.*?src=javascript:)", "XSS (JS Injection)"),

    # Local File Inclusion / Directory Traversal
    (r"\.\./|\.\.\\", "Path Traversal / LFI"),

    # Remote File Inclusion
    (r"http[s]?://.*\.(php|txt|sh)", "RFI (Remote File Inclusion)"),

    # Command Injection
    (r";\s*(cat|ls|whoami|id|wget|curl|nc|bash|sh)", "Command Injection"),
    (r"`.*?`", "Command Injection (Backticks)"),

    # PHP/RFI Shells
    (r"\?cmd=|\?exec=|\?shell=", "Web Shell Access"),

    # SSTI (Server-Side Template Injection)
    (r"\{\{.*?\}\}", "SSTI"),

    # LDAP Injection
    (r"\(|\)|\*|\&|\|", "LDAP Injection"),

    # XML External Entity
    (r"<!DOCTYPE\s+[^>]*\s+\[.*?ENTITY", "XXE (XML External Entity)"),

    # SSRF
    (r"http://127\.0\.0\.1|http://localhost", "SSRF"),

    # Other
    (r"base64_decode\(|eval\(|system\(", "Code Execution / Obfuscation"),
]