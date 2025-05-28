import os
import tempfile
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from utils.helper import load_env

# Carrega variáveis de ambiente
load_env()

class TelegramBot:
    
    def __init__(self, callback, callback_foto=None, saudacao: str = "Olá! Seja bem-vindo!"):
        self.saudacao = saudacao
        self.TOKEN = os.getenv('TELEGRAM_API_TOKEN')

        if not self.TOKEN:
            raise ValueError("Erro: TELEGRAM_API_TOKEN não foi encontrado no .env")

        self.message_handler = callback  # Callback para processar mensagens
        self.photo_handler = callback_foto  # Callback opcional para processar imagens
        
        # Inicializa a aplicação
        self.application = Application.builder().token(self.TOKEN).build()
        
        # Adiciona os handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_message))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.get_photo))  # Captura imagens
        self.application.add_handler(MessageHandler(filters.VIDEO, self.get_photo))  # Captura imagens
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.get_file))

    def start(self, update: Update, context):
        """Responde ao comando /start com uma mensagem de boas-vindas"""
        user = update.effective_user
        update.message.reply_html(
            f"{self.saudacao} {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def get_file(self, update: Update, context):
        message = update.message
        i=0


    async def get_message(self, update: Update, context):
        """Processa mensagens de texto enviadas pelo usuário"""
        user_message = update.message.text
        response = await self.message_handler(user_message)  # Adicionamos `await`
        await update.message.reply_text(response)  # Adicionamos `await`


    async def get_photo(self, update: Update, context):
        """Recebe fotos e a legenda (se houver)"""
        file_id = update.message.photo[-1].file_id  # Pega a melhor qualidade da foto
        caption = update.message.caption  # Captura a legenda (se houver)

        user = update.message.from_user
        photo_file = await context.bot.get_file(file_id)  
                
        temp_dir = tempfile.gettempdir()
        file_name = os.path.join(temp_dir, f"{user.id}-{file_id}.png")
        
        await photo_file.download_to_drive(file_name)  # Use await no download

        print(f"Imagem salva como: {file_name}")  # Log para depuração

        
        ret = ""
        if self.photo_handler:
            ret = await self.photo_handler(file_name, caption)  # Passa a foto para o callback
        
        await update.message.reply_text(ret)  # Envia resposta

    def run(self):
        """Inicia o bot usando polling"""
        print("🤖 Bot Telegram rodando...")
        self.application.run_polling()
