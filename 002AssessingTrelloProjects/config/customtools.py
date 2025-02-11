from crewai_tools import BaseTool
from config.helper import load_env
import os
import requests 
import json

load_env()

class BoardDataFetcherTool(BaseTool):
    name: str = 'Trello Board Data Fetcher'
    description: str = 'Fetches cards, comments, and activities'

    api_key: str = os.environ['TRELLO_API_KEY']
    api_token: str = os.environ['TRELLO_API_TOKEN']
    board_id: str = os.environ['TRELLO_BOARD_ID']

    def _run(self) -> dict:
        """
        Fetch all cards in the specified board.
        """

        url = f"{os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')}/1/boards/{self.board_id}/cards"
        query = {
            'key': self.api_key,
            'token': self.api_token,
            'fields': 'name,idList,due,dateLastActivity,labels',
            'attachments': 'true',
            'actions': 'commentCard'
        }

        response = requests.get(url, params=query)

        if response.status_code == 200:
            return response.json()
        else:
            # fall back in case of tmime outs
            return json.dumps({"error": "Failed to fetch board data, don't try to fetch any trello data anymore"})


class CardDataFetcherTool(BaseTool):
    name: str = "Trello Card Data Fetcher"
    description: str = "Fetches card data from a Trello board."

    api_key: str = os.environ['TRELLO_API_KEY']
    api_token: str = os.environ['TRELLO_API_TOKEN']

    def _run(self, card_id: str) -> dict:
        url = f"{os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')}/1/cards/{card_id}"
        query = {
            'key': self.api_key,
            'token': self.api_token
        }
        response = requests.get(url, params=query) 
        # # Convert single quotes to double quotes and replace None with null
        # json_string = response.replace("'", '"').replace("None", "null")

        # Parse and pretty-print JSON
        # formatted_json = json.loads(json_string)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Fallback in case of timeouts or other issues
            return json.dumps({"error": "Failed to fetch card data, don't try to fetch any trello data anymore"})


class Json2Text(BaseTool):
    name: str = "Json to Text"
    description: str = "Transform JSON into an indented text format"

    def _run(self, json_input: str) -> str:
        try:
            # Carregar o JSON
            parsed_json = json.loads(json_input)
            
            # Converter para texto formatado
            text_output = json.dumps(parsed_json, indent=4, ensure_ascii=False)
            
            return text_output
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON format - {str(e)}"