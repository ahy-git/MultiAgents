from crewai.tools import tool
import requests

@tool
def searxng_search(query: str) -> str:
    """
    Search the web using a locally hosted SearxNG instance.
    Args:
        query (str): Search term
    Returns:
        str: Top results
    """
    SEARXNG_URL = "http://localhost:8887/search"
    params = {'q': query, 'format': 'json'}
    response = requests.get(SEARXNG_URL, params=params)

    if response.status_code == 200:
        results = response.json()
        return "\n".join(
            f"{res['title']} - {res['url']}" for res in results['results']
        )
    else:
        return f"Error: {response.status_code}"