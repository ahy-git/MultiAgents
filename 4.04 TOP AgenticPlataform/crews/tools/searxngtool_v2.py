from crewai.tools import tool
import requests
from datetime import datetime

@tool
def searxng_search(query: str, tema: str = "geral", data_inicio: str = "", limite: int = 20) -> str:
    """
Executa uma busca na web utilizando o mecanismo SearxNG, 
adaptada ao contexto temático e temporal da consulta.
Parâmetros esperados:
    - query (str): É a pergunta ou termo principal que será buscado. Exemplo: "impacto da IA na educação".
    - tema (str): Define o tipo de fontes que o agente deseja consultar. As opções são:
        - "geral": busca em mecanismos amplos como Google e Bing.
        - "noticias": foca em portais de notícias como Google News, BBC e Bing News.
        - "cientifico": retorna resultados de artigos e papers em bases como arXiv e Semantic Scholar.
        - "tecnico": busca conteúdos técnicos em fontes como Stack Overflow, GitHub e sites de documentação.
    - data_inicio (str): Um filtro opcional para limitar os resultados a publicações feitas **a partir dessa data**. Deve ser informada no formato "YYYY-MM-DD".
        Exemplo: "2023-01-01" retorna apenas conteúdos publicados após 1º de janeiro de 2023.
    - limite (int): Define quantos resultados devem ser retornados. Por padrão, traz os 5 principais resultados ordenados por relevância.
Retorno:
Uma string contendo uma lista formatada com os principais resultados, incluindo:
    - Título
    - Resumo (quando disponível)
    - URL
    - Fonte original (ex: Google, arXiv, GitHub)
O objetivo é permitir que o agente LLM tenha acesso rápido e filtrado a informações da web, 
com controle sobre o tema e período de interesse.
    """
    SEARXNG_URL = "http://localhost:8887/search"

    # Filtros por tema
    tema = tema.lower()
    categorias = {
        "geral": {"engines": "google,bing", "categoria": "general"},
        "noticias": {"engines": "google news,bbc,bing news", "categoria": "news"},
        "cientifico": {"engines": "arxiv,semantic scholar", "categoria": "science"},
        "tecnico": {"engines": "stack overflow,github,docs", "categoria": "it"},
    }

    config = categorias.get(tema, categorias["geral"])

    # Aplica filtro de data se informado
    if data_inicio:
        try:
            datetime.strptime(data_inicio, "%Y-%m-%d")
            query += f" after:{data_inicio}"
        except ValueError:
            return "[Erro] Formato de data inválido. Use AAAA-MM-DD."

    params = {
        'q': query,
        'format': 'json',
        'language': 'pt',
        'safesearch': 1,
        'categories': config["categoria"],
        'engines': config["engines"]
    }

    try:
        response = requests.get(SEARXNG_URL, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get('results', [])

        if not results:
            return "Nenhum resultado encontrado."

        return "\n\n".join(
            f"{res['title']}\n{res.get('content', '').strip()}\n{res['url']} (via {res['engine']})"
            for res in results[:limite]
        )

    except requests.RequestException as e:
        return f"[Erro de conexão] {str(e)}"
    except Exception as e:
        return f"[Erro inesperado] {str(e)}"
