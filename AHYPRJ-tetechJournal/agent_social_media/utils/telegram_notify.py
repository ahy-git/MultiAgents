import os
import requests
import time 

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CHAT_ID = "-4561347244"

def notify_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        time.sleep(2)
    except Exception as e:
        print(f"❌ Falha ao enviar mensagem para o Telegram: {e}", flush=True)
