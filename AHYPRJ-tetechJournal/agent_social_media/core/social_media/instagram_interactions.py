import os
import requests
from dotenv import load_dotenv

class InstagramInteractions:
    """
    Classe para interagir com o Instagram, permitindo verificar comentários e mensagens diretas (DMs).
    """
    load_dotenv()

    def __init__(self):
        self.instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        self.base_url = f'https://graph.facebook.com/v22.0/{self.instagram_account_id}'
        self.access_token = os.getenv("INSTAGRAM_API_KEY")

    def get_comments(self, post_id, limit=10):
        """
        Obtém os últimos comentários de um post no Instagram.

        :param post_id: ID do post no Instagram.
        :param limit: Número máximo de comentários a serem retornados.
        :return: Lista de comentários.
        """
        print(f"📥 Obtendo os últimos {limit} comentários do post {post_id}...")

        url = f'{self.base_url}_{post_id}/comments'
        params = {
            'access_token': self.access_token,
            'fields': 'id,text,from',
            'limit': limit
        }

        response = requests.get(url, params=params)
        response_data = response.json()

        if 'data' not in response_data:
            print(f"❌ Erro ao buscar comentários: {response_data}")
            return []

        comments = response_data['data']
        for comment in comments:
            user = comment['from']['username'] if 'from' in comment else "Usuário desconhecido"
            print(f"💬 @{user}: {comment['text']}")

        return comments

    def get_direct_messages(self, limit=10):
        """
        Obtém as últimas mensagens diretas (DMs) recebidas na conta do Instagram.

        :param limit: Número máximo de mensagens a serem retornadas.
        :return: Lista de mensagens diretas.
        """
        print(f"📥 Obtendo as últimas {limit} mensagens diretas...")

        url = f'https://graph.facebook.com/v22.0/me/conversations'
        params = {
            'access_token': self.access_token,
            'fields': 'id,participants,messages.limit(1){message,from,created_time}',
            'limit': limit
        }

        response = requests.get(url, params=params)
        response_data = response.json()

        if 'data' not in response_data:
            print(f"❌ Erro ao buscar mensagens diretas: {response_data}")
            return []

        messages = response_data['data']
        for msg in messages:
            sender = msg['messages']['data'][0]['from']['name']
            message_text = msg['messages']['data'][0]['message']
            print(f"📩 {sender}: {message_text}")

        return messages
    