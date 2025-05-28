import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Diretório onde os posts estão armazenados
ASSETS_DIR = os.path.join(os.getcwd(), "assets")

# Credenciais do Instagram
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")
