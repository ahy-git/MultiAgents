##FAILED! WE MUST FIND A BETTER SCRAPE SOLUTION

import subprocess
from crewai.tools import BaseTool

class SpiderCustom(BaseTool):
    name: str = "Spider CLI Tool"
    description: str = """
    Esta ferramenta executa o binário spider-rs (spider_cli) dentro 
    de um container Docker, realizando uma varredura automatizada (web crawling)
    a partir de uma URL fornecida. A ferramenta segue os links encontrados
    na página inicial até a profundidade especificada, coletando e 
    retornando metadados das páginas rastreadas, como URLs descobertas,
    status HTTP e tempo de resposta. É ideal para agentes que precisam mapear
    dinamicamente a estrutura de um site, identificar rotas acessíveis ou 
    coletar informações para tarefas de análise, monitoramento ou extração de dados.

    Inputs esperados:
    - url (str): URL de entrada a ser rastreada, com protocolo (https://)
    - depth (int, opcional): profundidade máxima de navegação entre links internos (padrão: 2)
    
    Formato de retorno:
    -(str): saída textual gerada pelo binário spider_cli, contendo o log da varredura, lista de URLs acessadas, status HTTP e outras informações técnicas relevantes.
    """

    def _run(self, url: str, depth: int = 2) -> str:
        try:
            result = subprocess.run(
                [
                    "docker", "exec", "spider-rs",
                    "./target/release/spider_cli",
                    "--url", url,
                    "--depth", str(depth)
                ],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Erro: {str(e)}"
