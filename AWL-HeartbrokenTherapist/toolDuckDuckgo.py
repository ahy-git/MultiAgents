# duckduckgo_tool.py
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class DuckDuckGoInput(BaseModel):
    query: str = Field(..., description="The search query to perform using DuckDuckGo.")

class DuckDuckGoTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "Use this tool to perform web searches via DuckDuckGo and retrieve summarized search results."
    args_schema: Type[BaseModel] = DuckDuckGoInput

    def _run(self, query: str) -> str:
        try:
            url = f"https://duckduckgo.com/html/?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Simple parse of result titles (this is NOT scraping JS-rendered results)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('a', class_='result__a', limit=5)
            links = [r.get_text() for r in results]

            if links:
                return "\n".join(links)
            return "No results found."

        except Exception as e:
            return f"Error while searching DuckDuckGo: {e}"

if __name__ == "__main__":
    tool = DuckDuckGoTool()
    input_query = {"query": "CrewAI multi-agent framework"}
    output = tool.run(input_query)
    print("\n🔍 DuckDuckGo Results:\n")
    print(output)