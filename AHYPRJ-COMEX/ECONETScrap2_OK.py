###############################################################
###############################################################
################## SCRAPE ####################################
###############################################################
from urllib.parse import quote_plus
import requests
from dotenv import load_dotenv
import os

load_dotenv
# Inicia sessão
session = requests.Session()

# Login
login_url = "https://comex.econeteditora.com.br/log.php"
payload = {
    "Log": os.getenv("LOGIN"),
    "Sen": os.getenv("PW"),
    "Pag": "/tec/index.php"
}
response_login = session.post(login_url, data=payload)
print("Login:", response_login.status_code)

# Passa pelo proxy para garantir ativação da interface
url_proxy = (
    "https://comex.econeteditora.com.br/usuarios_online.php"
    "?url=https://comex.econeteditora.com.br/tec/index.php?"
    "form[ncm]=&form[palavra]=moto&form[botao]=Pesquisar&form[acao]=pesquisar"
)
session.get(url_proxy)  # não precisa armazenar, só ativar a sessão corretamente

# Agora, com a sessão ativa, faz a chamada AJAX direta
get_php = 'a:1:{s:4:"form";a:4:{s:3:"ncm";s:0:"";s:7:"palavra";s:4:"moto";s:5:"botao";s:9:"Pesquisar";s:4:"acao";s:9:"pesquisar";}}'
url_ajax = (
    "https://comex.econeteditora.com.br/tec/load_tabs_importacao.php?"
    f"form[acao]=pesquisar&get={quote_plus(get_php)}"
)

headers_ajax = {
    "Referer": "https://comex.econeteditora.com.br/tec/index.php",
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Cache-Control": "no-cache"
}

response_final = session.get(url_ajax, headers=headers_ajax)
print("Status:", response_final.status_code)
print(response_final.text[:3000])
