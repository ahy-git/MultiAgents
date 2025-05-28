import requests
from crewai.tools import BaseTool

class RemoteScraperTool(BaseTool):
    name : str = "Remote Scraper Tool"
    description : str = """
    Ferramenta que envia uma URL para um serviço HTTP local que realiza scraping
    e retorna o resumo da página. Ideal para coletar o conteúdo dinâmico
    de sites que utilizam JavaScript. A URL deve ser passada como string.
    
    Input esperado:
    - url (str): A URL codificada da página a ser raspada

    Retorno:
    - (str): Conteudo renderizado da página como texto em formato md.
    """

    def _run(self, url: str) -> str:
        try:
            response = requests.get(
                f"http://localhost:1111/scrape?url={url}",
                timeout=30
            )
            if response.status_code == 200:
                return response.text
            else:
                return f"Erro {response.status_code}: {response.text}"
        except Exception as e:
            return f"Erro ao acessar o serviço remoto: {str(e)}"
