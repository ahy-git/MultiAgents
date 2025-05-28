
import requests

# Sessão para manter cookies
session = requests.Session()

# URL de login
login_url = "https://comex.econeteditora.com.br/index.php"

# Dados do formulário
payload = {
    "Log": "GDC61910",
    "Sen": "dan8278",
    "Pag": "comex_login2"
}

# Envia o POST de login
response = session.post(login_url, data=payload)

# print(f'{response}')  # Deve imprimir <Response [200]>
# print("Cookies após login:", session.cookies.get_dict())

# Verifica acesso à página protegida
protected_url = "https://comex.econeteditora.com.br/usuarios_online.php?url=https://comex.econeteditora.com.br/inicio.php"
headers = {
    "Referer": "https://comex.econeteditora.com.br/index.php",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

protected_response = session.get(protected_url, headers=headers)

# Verifica parte do conteúdo da resposta
# print("Status acesso protegido:", protected_response.status_code)
# print("Trecho da resposta protegida:")
# print(protected_response.text[:1000])  # Mostra os primeiros 1000 caracteres da página protegida

def acessar_com_autenticacao(url_interna: str):
    base_proxy_url = "https://comex.econeteditora.com.br/usuarios_online.php"
    full_url = f"{base_proxy_url}?url={url_interna}"

    headers = {
        "Referer": "https://comex.econeteditora.com.br/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = session.get(full_url, headers=headers)
    # print(f"Status: {response.status_code}")
    # print(response.text[:1000])  # Conteúdo parcial para validação

    return response.text

# URL interna desejada
importacao_url_interna = "/tec/load_tabs_importacao.php?form[acao]=&get=a:0:{}"

# Acessa a aba de importação via proxy de autenticação
conteudo_importacao = acessar_com_autenticacao(importacao_url_interna)

# Se quiser imprimir ou tratar o conteúdo:
# print("Conteúdo da aba de importação:")
# print(conteudo_importacao[:2000])  # Imprime os primeiros 2000 caracteres para análise

def pesquisar_termo(termo: str):
    pesquisa_url_interna = (
        f"/tec/index.php?form[ncm]=&form[palavra]={termo}&form[botao]=Pesquisar&form[acao]=pesquisar"
    )
    return acessar_com_autenticacao(pesquisa_url_interna)


termo = "moto"
conteudo = pesquisar_termo(termo)
# print (f"Termo buscado:{termo}")
# print(conteudo[:2000])
# String serializada PHP para o termo "moto"
serial_fixo = 'a:1:{s:4:"form";a:4:{s:3:"ncm";s:0:"";s:7:"palavra";s:4:"moto";s:5:"botao";s:9:"Pesquisar";s:4:"acao";s:9:"pesquisar";}}'

# URL interna da aba importação com o parâmetro serializado
url_interna_importacao = f"/tec/load_tabs_importacao.php?form[acao]=pesquisar&get={serial_fixo}"

# Faz o acesso via proxy autenticado
resultado_html = acessar_com_autenticacao(url_interna_importacao)

# Mostra parte do conteúdo
print("Resultado parcial:\n")
print(resultado_html[:3000])
