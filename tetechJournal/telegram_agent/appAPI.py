# to be used in DOCKER

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crew_conversa import ChatAgent
from telegramBotAhyAPI import TelegramBot


async def gerenciar_mensagem(message: str) -> str:
    """Função que será registrada no bot para processar mensagens."""    
    inputs = {"message": message}
    agent_text = agent.kickoff(inputs=inputs)
    return agent_text

# async def gerenciar_foto(image_path, caption):
#     """Recebe e processa uma foto enviada pelo usuário."""  

#     InstagramSend.send_instagram(image_path, caption)
    
#     return  f"📸 Foto salva da {caption}."
 
async def gerenciar_logs(log_message: str) -> None:
    """Função para enviar logs do bot diretamente para o Telegram."""
    return log_message  # Retorna a string para ser enviada ao usuário no Telegram
   


if __name__ == "__main__":
    
    agent = ChatAgent()
    
    bot = TelegramBot(
        callback=gerenciar_mensagem,
        # callback_foto=gerenciar_foto,  # Agora também recebe imagens
        saudacao="Olá doidera"
    )
    bot.run()
