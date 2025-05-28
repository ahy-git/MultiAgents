# to be used in docker
import os
import tempfile
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from utils.helper import load_env
from datetime import datetime
import asyncio
import subprocess
import shutil
import sys
import httpx
import traceback

# Carrega variáveis de ambiente
load_env()


class TelegramBot:

    def __init__(self, callback, callback_foto=None, saudacao: str = "Olá! Seja bem-vindo!"):
        self.saudacao = saudacao
        self.TOKEN = os.getenv('TELEGRAM_API_TOKEN')

        if not self.TOKEN:
            raise ValueError(
                "Erro: TELEGRAM_API_TOKEN não foi encontrado no .env")

        self.message_handler = callback  # Callback para processar mensagens
        self.photo_handler = callback_foto  # Callback opcional para processar imagens

        # Inicializa a aplicação
        self.application = Application.builder().token(self.TOKEN).build()

        # Adiciona os handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help",self.help_message))
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.get_message))
        self.application.add_handler(MessageHandler(
            filters.PHOTO | filters.Document.IMAGE, self.get_photo))  # Captura imagens
        self.application.add_handler(MessageHandler(
            filters.VIDEO, self.get_photo))  # Captura imagens
        self.application.add_handler(MessageHandler(
            filters.Document.ALL, self.get_file))

    def start(self, update: Update, context):
        """Responde ao comando /start com uma mensagem de boas-vindas"""
        user = update.effective_user
        update.message.reply_html(
            f"{self.saudacao} {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )
   
    def format_path_for_api(self,local_path: str) -> str:
        """
        Converte um caminho local em um caminho válido dentro do container Docker.
        Se estiver rodando localmente, retorna o caminho original.
        Se estiver rodando em Docker, converte para o path do volume montado.
        """
        local_path = os.path.abspath(local_path)
        
        if os.getenv("RUNNING_IN_DOCKER") == "1":
            # Converte para path relativo a partir da pasta montada
            docker_path = local_path.replace("\\", "/").split("/agent_social_media", 1)[-1]
            return f"/agent_social_media{docker_path}"
        
        return local_path
    
    async def chamar_api_autopost(self, tipo: str, pasta: str):
        """
        Chama a API do serviço agent_social_media de forma assíncrona para processar a pasta fornecida.

        :param tipo: 'story' ou 'post'
        :param pasta: caminho completo da pasta (dentro do volume compartilhado)
        """
        # url = f"http://autopost_service:1113/process/{tipo}"
        API_HOST = os.getenv("AUTOPOST_API_HOST_DOCKER", "localhost")  
        # API_HOST = os.getenv("AUTOPOST_API_HOST", "localhost")  # fallback para localhost
        API_PORT = os.getenv("AUTOPOST_API_PORT", "1113")
        url = f"http://{API_HOST}:{API_PORT}/process/{tipo}"

        
        payload = {"folder_path": pasta}
        print(payload)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                print(f"❌ Erro na requisição: {e}")
                print("URL:", url)
                print("Payload:", payload)
                print("Traceback:")
                traceback.print_exc()
                return {"error": str(e)}
            except httpx.HTTPStatusError as e:
                print(f"❌ Erro HTTP: {e}")
                return {"error": str(e)}
        
    async def get_file(self, update: Update, context):
        message = update.message
        i = 0

    async def monitor_log_file(update, context, log_file="../agent_social_media/autopost.log"):
        """Monitora o arquivo de log e envia novas linhas ao Telegram sempre que forem adicionadas."""

        if not os.path.exists(log_file):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="🚫 Nenhum log encontrado para autopost.py.")
            return

        await context.bot.send_message(chat_id=update.effective_chat.id, text="📡 Monitorando logs do autopost.py...")

        with open(log_file, "r", encoding="utf-8") as log:
            log.seek(0, os.SEEK_END)  # Move o cursor para o final do arquivo

            while True:
                line = log.readline()
                if line:
                    line = line.strip()
                    if line:
                        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"📜 **Novo log:**\n```\n{line}\n```", parse_mode="Markdown")

                # Aguarda 1 segundo antes de verificar novamente
                await asyncio.sleep(1)

    async def get_message(self, update: Update, context):
        """Processa mensagens de texto enviadas pelo usuário"""
        user_message = update.message.text
        # Adicionamos `await`
        response = await self.message_handler(user_message)
        await update.message.reply_text(response)  # Adicionamos `await`
        
  
    async def help_message(self, update: Update, context):
        help_message = """
🤖 *Bot de Automação de Conteúdo para Telegram*

Este bot foi criado para automatizar a criação de conteúdo para *posts* e *stories* no Instagram, utilizando inteligência artificial para gerar legendas com base em imagens enviadas.

---

📌 *Comandos Disponíveis*

*/help*  
Exibe esta lista de comandos com explicações rápidas.

---

🖼️ *Comandos para Geração de Legendas (requer imagem)*

*/post*  
- Gera uma legenda completa para um *post de feed* no Instagram.  
- Analisa a imagem com IA e cria um texto criativo e bem-humorado.  
- O conteúdo é estruturado com emojis, tom inteligente e hashtags.  
- Após a geração, o `autopost_service` publica automaticamente no Instagram.

*/stories*  
- Gera uma legenda curta para *story* no Instagram.  
- Texto mais direto, descontraído e expressivo.
- Edita a imagem com IA, adicionando texto, ajustando tamanho, etc  
- Publica automaticamente usando o `autopost_service`.

---

Se nenhuma imagem for detectada, o bot avisará o usuário.
"""

        await update.message.reply_text(help_message, parse_mode="Markdown")
        return
    
    async def get_photo(self, update: Update, context: CallbackContext):
        """Recebe fotos e a legenda (se houver) e roteia para diferentes ações."""
        file_id = None  # Inicializa a variável para evitar erro de referência

        # 📸 Se a imagem foi enviada como foto
        if update.message.photo:
            # Usa a melhor qualidade disponível
            file_id = update.message.photo[-1].file_id

        # 📁 Se a imagem foi enviada como documento (e for um arquivo de imagem)
        elif update.message.document and update.message.document.mime_type.startswith("image/"):
            # Captura o file_id do documento enviado
            file_id = update.message.document.file_id

        # ❌ Se nenhum arquivo de imagem foi detectado
        if not file_id:
            await update.message.reply_text("� Nenhuma imagem detectada! Envie uma foto ou um documento de imagem.")
            return

        caption = update.message.caption or ""  # Captura a legenda (se houver)
        user = update.message.from_user
        # Define um diretório TEMP mais seguro no mesmo disco do destino (D:)
        temp_dir = "./temp_bot"
        os.makedirs(temp_dir, exist_ok=True)

        # Baixa o arquivo temporário
        photo_file = await context.bot.get_file(file_id)
        file_name = os.path.join(temp_dir, f"{user.id}-{file_id[-4:]}.png")
        await photo_file.download_to_drive(file_name)

        print(f"Imagem salva como: {file_name}")  # Log para depuração
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"📸 Foto recebida!"
        )

        # Dicionário de rotas baseado nos comandos do caption
        command_handlers = {
            "/stories": self.handle_stories,
            "/post": self.handle_posts
        }

        # Identifica o comando no caption
        command = caption.split()[0] if caption.startswith("/") else None

        if command in command_handlers:
            # Executa a função correspondente
            await command_handlers[command](update, context, file_name, caption)
        else:
            # Processamento normal da foto
            ret = await self.photo_handler(file_name, caption) if self.photo_handler else "Imagem recebida."
            await update.message.reply_text(ret)

    async def handle_stories(self, update: Update, context: CallbackContext,  file_name, caption):
        """Processa imagens para stories, criando a pasta e armazenando a imagem e descrição."""
        today_str = datetime.today().strftime("%Y%m%d")
        base_dir = os.path.abspath(os.path.join(
            "..", "agent_social_media", "assets"))

        # Busca um número disponível para a pasta
        index = 1
        while True:
            stories_folder = os.path.join(
                base_dir, f"{today_str}_stories_{index:03d}")
            if not os.path.exists(stories_folder):
                os.makedirs(stories_folder)  # Cria a pasta
                break
            index += 1

        # Move a imagem para a pasta criada
        new_file_path = os.path.join(
            stories_folder, os.path.basename(file_name))

        shutil.move(file_name, new_file_path)

        # Para mesmos volumes ou rodando localmente usar: os.rename e' mais rapido
        # os.rename(file_name, new_file_path)

        # Cria o arquivo `description.txt` com o texto após "/stories"
        description_path = os.path.join(stories_folder, "description.txt")
        with open(description_path, "w", encoding="utf-8") as desc_file:
            desc_file.write(caption.replace("/stories", "").strip())

        print(f"Imagem e descrição salvas em: {stories_folder}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Imagem e descrição salvas em: {stories_folder}"
        )
        
       # 🔗 Chama API do autopost_service
        folder_path_docker = self.format_path_for_api(stories_folder)
        result = await self.chamar_api_autopost("story", folder_path_docker)
        print(result)

        # ✅ Inicia o monitoramento do log
        # await self.monitor_log_file(update, context, "../agent_social_media/autopost.log")

    async def handle_posts(self,  update: Update, context: CallbackContext, file_name, caption):
        """Processa imagens para stories, criando a pasta e armazenando a imagem e descrição."""
        today_str = datetime.today().strftime("%Y%m%d")
        base_dir = os.path.abspath(os.path.join(
            "..", "agent_social_media", "assets"))

        # Busca um número disponível para a pasta
        index = 1
        while True:
            post_folder = os.path.join(
                base_dir, f"{today_str}_post_{index:03d}")
            if not os.path.exists(post_folder):
                os.makedirs(post_folder)  # Cria a pasta
                break
            index += 1

        # Move a imagem para a pasta criada
        new_file_path = os.path.join(post_folder, os.path.basename(file_name))

        shutil.move(file_name, new_file_path)

        # Usar os.rename se no mesmo volume ou rodando local
        # os.rename(file_name, new_file_path)

        # Cria o arquivo `caption.txt` com o texto após "/posts"
        description_path = os.path.join(post_folder, "caption.txt")
        with open(description_path, "w", encoding="utf-8") as desc_file:
            desc_file.write(caption.replace("/post", "").strip())

        print(f"Imagem e descrição salvas em: {post_folder}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Imagem e descrição salvas Chat ID: {update.effective_chat.id}"
        )

        # 🔗 Chama API do autopost_service
        folder_path_docker = self.format_path_for_api(post_folder)
        result = await self.chamar_api_autopost("post", post_folder)
        print(result)

    def run(self):
        """Inicia o bot usando polling"""
        print("🤖 Bot Telegram rodando...")
        self.application.run_polling()
