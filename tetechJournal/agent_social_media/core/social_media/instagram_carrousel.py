import os
import time
from infra.imgur.imgur_service import ImageUploader
from core.social_media.instagram_post import InstagramPostService

class InstagramCarouselPost:
    def __init__(self):
        self.uploader = ImageUploader()
        self.instagram = InstagramPostService()

    def post_carousel(self, image_paths, caption):
        """
        Publica um carrossel no Instagram com múltiplas imagens.
        
        :param image_paths: Lista de caminhos das imagens a serem postadas.
        :param caption: Texto da legenda do post.
        :return: ID do post publicado ou None em caso de erro.
        """
        if len(image_paths) < 2:
            print("❌ O carrossel deve conter pelo menos duas imagens.")
            return None

        uploaded_images = []
        delete_hashes = []

        # Faz upload de todas as imagens para o Imgur
        print("📤 Enviando imagens para Imgur...")
        for image_path in image_paths:
            response = self.uploader.upload_from_path(image_path)
            if response and "url" in response:
                uploaded_images.append(response["url"])
                delete_hashes.append(response["deletehash"])
            else:
                print(f"❌ Falha ao enviar {image_path} para Imgur.")
                return None  # Se uma falhar, aborta a postagem

        print(f"✅ Todas as imagens foram enviadas: {uploaded_images}")

        # Criar um contêiner de mídia para cada imagem
        media_container_ids = []
        for img_url in uploaded_images:
            media_id = self.instagram.create_media_container(img_url, caption if img_url == uploaded_images[0] else "")
            if media_id:
                media_container_ids.append(media_id)
            else:
                print(f"❌ Falha ao criar contêiner para {img_url}.")
                return None

        print(f"✅ Contêineres criados: {media_container_ids}")

        # Publica o carrossel
        post_id = self.instagram.publish_carousel(media_container_ids)

        if post_id:
            print(f"✅ Carrossel publicado com sucesso! Post ID: {post_id}")

            # Remover imagens do Imgur após a postagem
            for delete_hash in delete_hashes:
                self.uploader.delete_image(delete_hash)

            return post_id
        else:
            print("❌ Falha ao publicar o carrossel.")
            return None
