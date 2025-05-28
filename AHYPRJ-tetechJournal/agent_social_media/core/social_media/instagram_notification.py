import os
import requests
from dotenv import load_dotenv

class InstagramNotifications:
    """
    Classe para monitorar notificações do Instagram, incluindo novos comentários, DMs e menções.
    """
    load_dotenv()

    def __init__(self):
        self.instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        self.base_url = f'https://graph.facebook.com/v22.0/{self.instagram_account_id}'
        self.access_token = os.getenv("INSTAGRAM_API_KEY")

    def get_recent_comments(self, limit=5):
        """ Obtém os últimos comentários nos posts do Instagram. """
        print("🔔 Buscando novos comentários...")

        url = f'{self.base_url}/media'
        params = {
            'access_token': self.access_token,
            'fields': 'id,caption',
            'limit': 5  # Últimos 5 posts
        }

        response = requests.get(url, params=params)
        response_data = response.json()

        if 'data' not in response_data:
            print(f"❌ Erro ao buscar posts: {response_data}")
            return []

        new_comments = []
        for post in response_data['data']:
            post_id = post['id']
            comments = self.get_comments(post_id, limit)

            if comments:
                new_comments.extend(comments)

        return new_comments

    def get_recent_dms(self, limit=5):
        """ Obtém as últimas mensagens diretas recebidas. """
        print("🔔 Buscando novas mensagens diretas...")

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

        return response_data['data']

    def get_mentions(self, limit=5):
        """ Obtém as últimas menções à conta do Instagram. """
        print("🔔 Buscando menções recentes...")

        url = f'{self.base_url}/tags'
        params = {
            'access_token': self.access_token,
            'fields': 'id,caption',
            'limit': limit
        }

        response = requests.get(url, params=params)
        response_data = response.json()

        if 'data' not in response_data:
            print(f"❌ Erro ao buscar menções: {response_data}")
            return []

        return response_data['data']

    def get_all_notifications(self):
        """ Obtém todas as notificações recentes. """
        print("🔔 Buscando todas as notificações...")
        comments = self.get_recent_comments()
        dms = self.get_recent_dms()
        mentions = self.get_mentions()

        return {
            "comments": comments,
            "direct_messages": dms,
            "mentions": mentions
        }
