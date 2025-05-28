###############################################################
################## SCRAPE COM SERIALIZAÇÃO DINÂMICA ##########
###############################################################

from urllib.parse import quote_plus
import requests
import phpserialize

def gerar_parametro_get(termo: str) -> str:
    form_dict = {
        "form": {
            "ncm": ncm,
            "palavra": termo,
            "botao": "Pesquisar",
            "acao": "pesquisar"
        }
    }
    return quote_plus(phpserialize.dumps(form_dict).decode("utf-8"))

# Termo desejado
termo = "moto"
ncm = ""

# Inicia sessão
session = requests.Session()

# Login via log.php
login_url = "https://comex.econeteditora.com.br/log.php"
payload = {
    "Log": "GDC61910",
    "Sen": "dan8278",
    "Pag": "/tec/index.php"
}
response_login = session.post(login_url, data=payload)
print("Login:", response_login.status_code)

# Ativa a interface simulando o clique de busca
url_proxy = (
    "https://comex.econeteditora.com.br/usuarios_online.php"
    f"?url=https://comex.econeteditora.com.br/tec/index.php?"
    f"form[ncm]=&form[palavra]={termo}&form[botao]=Pesquisar&form[acao]=pesquisar"
)
session.get(url_proxy)

# Gera o parâmetro get dinamicamente
get_php = gerar_parametro_get(termo)

# Requisição AJAX com dados da aba de importação
url_ajax = (
    "https://comex.econeteditora.com.br/tec/load_tabs_importacao.php?"
    f"form[acao]=pesquisar&get={get_php}"
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

# Exibe o conteúdo da resposta
print("Status:", response_final.status_code)
print(response_final.text[:1000])

from bs4 import BeautifulSoup
import json

def extrair_tabela_para_json(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    
    # Tenta encontrar a primeira tabela — pode adaptar com id/class se necessário
    tabela = soup.find('table')
    if not tabela:
        return []

    # Captura o cabeçalho
    cabecalho = []
    thead = tabela.find('thead')
    if thead:
        cabecalho = [th.get_text(strip=True) for th in thead.find_all('th')]
    else:
        # se não tiver thead, tenta a primeira linha
        primeira_linha = tabela.find('tr')
        if primeira_linha:
            cabecalho = [td.get_text(strip=True) for td in primeira_linha.find_all(['th', 'td'])]

    # Captura os dados
    dados = []
    for linha in tabela.find_all('tr')[1:]:  # Pula o cabeçalho
        colunas = linha.find_all('td')
        if not colunas:
            continue
        valores = [td.get_text(strip=True) for td in colunas]
        item = dict(zip(cabecalho, valores))
        dados.append(item)

    return dados

responsejson = extrair_tabela_para_json(response_final.text)

print(responsejson[:1000])
with open("resultado_importacao.json", "w", encoding="utf-8") as f:
    json.dump(responsejson, f, ensure_ascii=False, indent=2)