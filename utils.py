from logger import save_log
from telegram import send_telegram

def save_log_and_send_telegram(msg):
    save_log(msg)
    send_telegram(msg)