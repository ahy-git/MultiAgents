from telegram import Update
from telegram.ext import Application, MessageHandler, filters

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_API_TOKEN")

async def print_chat_id(update: Update, context):
    print(f"✅ Chat ID: {update.effective_chat.id}")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, print_chat_id))
app.run_polling()
