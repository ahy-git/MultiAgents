from dotenv import load_dotenv
import requests
import os

load_dotenv()
chatID = os.getenv("TELEGRAM_CHAT_ID")
telegramAPIToken=os.getenv("TELEGRAM_API_TOKEN")
results = requests.post(f"https://api.telegram.org/bot{telegramAPIToken}/sendMessage", 
                data={"chat_id": chatID, "text": "Erro ao enviar processar resumo"})
print(results)
print(f"https://api.telegram.org/bot{telegramAPIToken}/sendMessage")
