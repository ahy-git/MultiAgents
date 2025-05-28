import os
import requests
from dotenv import load_dotenv

class InstagramPostService:
    load_dotenv()

    def __init__(self):
        self.instagram_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
        self.base_url = f'https://graph.facebook.com/v22.0/{self.instagram_account_id}'
        self.access_token = os.getenv("INSTAGRAM_API_KEY")

    def create_media_container(self, image_url, caption):
        """
        Cria um contêiner de mídia para o post.
        :param image_url: URL da imagem a ser postada.
        :param caption: Legenda da postagem.
        :return: ID do contêiner de mídia ou None em caso de erro.
        """
        url = f'{self.base_url}/media'
        payload = {
            'image_url': image_url,
            'caption': caption,
            'access_token': self.access_token
        }

        response = requests.post(url, data=payload)
        response_data = response.json()

        if 'id' not in response_data:
            print(f"Erro ao criar contêiner de mídia: {response_data}")
            return None

        return response_data['id']

    def publish_media(self, media_container_id):
        """
        Publica o contêiner de mídia no Instagram.
        :param media_container_id: ID do contêiner de mídia.
        :return: ID do post publicado ou None em caso de erro.
        """
        url = f'{self.base_url}/media_publish'
        payload = {
            'creation_id': media_container_id,
            'access_token': self.access_token
        }

        response = requests.post(url, data=payload)
        response_data = response.json()

        if 'id' not in response_data:
            print(f"Erro ao publicar o post: {response_data}")
            return None

        print(f"Post publicado com sucesso! ID do Post: {response_data['id']}")
        return response_data['id']

    def post_image(self, image_url, caption):
        """
        Faz todo o fluxo de criação e publicação de um post no Instagram.
        :param image_url: URL da imagem a ser postada.
        :param caption: Legenda da postagem.
        :return: ID do post publicado ou None em caso de erro.
        """
        print("Iniciando publicação de imagem no Instagram...")

        media_container_id = self.create_media_container(image_url, caption)
        if not media_container_id:
            print("Falha na criação do contêiner de mídia. Interrompendo o processo.")
            return None

        post_id = self.publish_media(media_container_id)
        if not post_id:
            print("Falha na publicação do post.")
            return None

        print(f"Processo concluído com sucesso! ID do Post: {post_id}")
        return post_id
    
    def post_story(self, image_url):
        """
        Publica uma imagem nos Stories do Instagram.

        :param image_url: URL da imagem a ser postada nos Stories.
        :return: ID do Story publicado ou None em caso de erro.
        """
        print("📲 Iniciando publicação do Story no Instagram...")

        url = f"{self.base_url}/media"
        payload = {
            "image_url": image_url,
            "media_type": "STORIES",
            "access_token": self.access_token
        }

        response = requests.post(url, data=payload)
        response_data = response.json()

        if "id" not in response_data:
            print(f"❌ Erro ao criar o Story: {response_data}")
            return None

        media_id = response_data["id"]
        print(f"✅ Contêiner de mídia criado para Story: {media_id}")

        # Publicar o Story
        publish_url = f"{self.base_url}/media_publish"
        publish_payload = {
            "creation_id": media_id,
            "access_token": self.access_token
        }

        publish_response = requests.post(publish_url, data=publish_payload)
        publish_response_data = publish_response.json()

        if "id" not in publish_response_data:
            print(f"❌ Erro ao publicar o Story: {publish_response_data}")
            return None

        story_id = publish_response_data["id"]
        print(f"✅ Story publicado com sucesso! ID do Story: {story_id}")
        return story_id
    
    def post_reels(self, video_url, caption):
        """
        Publica um vídeo nos Reels do Instagram.

        :param video_url: URL do vídeo a ser postado.
        :param caption: Legenda para o Reels.
        :return: ID do Reels publicado ou None em caso de erro.
        """
        print("📲 Iniciando publicação do Reels no Instagram...")

        # Criar um contêiner de mídia para o Reels
        url = f"{self.base_url}/media"
        payload = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS",
            "access_token": self.access_token
        }

        response = requests.post(url, data=payload)
        response_data = response.json()

        if "id" not in response_data:
            print(f"❌ Erro ao criar contêiner de mídia para Reels: {response_data}")
            return None

        media_id = response_data["id"]
        print(f"✅ Contêiner de mídia criado para Reels: {media_id}")

        # Publicar o Reels
        publish_url = f"{self.base_url}/media_publish"
        publish_payload = {
            "creation_id": media_id,
                        "access_token": self.access_token
                    }

        publish_response = requests.post(publish_url, data=publish_payload)
        publish_response_data = publish_response.json()

        if "id" not in publish_response_data:
            print(f"❌ Erro ao publicar o Reels: {publish_response_data}")
            return None

        reels_id = publish_response_data["id"]
        print(f"✅ Reels publicado com sucesso! ID do Reels: {reels_id}")
        return reels_id



