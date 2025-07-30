import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(ip, port, service, data, geo, threats=None):
    msg = (
        f"⚠️ *Honeypot Alert*\n"
        f"*IP:* {ip}\n"
        f"*Port:* {port} ({service})\n"
        f"*Data:* `{data}`\n"
        f"*Location:* {geo['country']}, {geo['city']} ({geo['isp']})"
    )
    if threats:
        msg += f"\n*Threats:* {', '.join(threats)}"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json=payload)
    except Exception as e:
        print(f"[!] Telegram error: {e}")
