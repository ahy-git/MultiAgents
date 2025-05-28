import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import base64
import tempfile
from utils.helper import load_env
from imgurpython import ImgurClient
import json

from config.paths import Paths

from PIL import Image
import io

class ImageUploader():
    def __init__(self):
        """
        Inicializa o cliente Imgur com as credenciais obtidas do arquivo .env.
        """
        load_env()
        print(os.getenv("IMGUR_CLIENT_ID"))
        self.client_id = os.getenv("IMGUR_CLIENT_ID")
        self.client_secret = os.getenv("IMGUR_CLIENT_SECRET")
        self.upload_url = "https://api.imgur.com/3/upload"  # Imgur API endpoint

        if not self.client_id or not self.client_secret:
            raise ValueError("As credenciais do Imgur não foram configuradas corretamente.")

        self.client = ImgurClient(self.client_id, self.client_secret)
        


    def upload_from_path(self, image_path: str) -> dict:
        """
        Faz o upload de uma imagem localizada no sistema de arquivos.

        :param image_path: Caminho absoluto da imagem a ser enviada.
        :return: Dicionário contendo id, url, e deletehash da imagem enviada.
        """
        
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"O arquivo especificado não foi encontrado: {image_path}")

        imgur_cache_path = os.path.join(os.path.dirname(image_path), ".imgurUpload")
        
        # Step 1️⃣: Check if `.imgurUpload` exists
        if os.path.exists(imgur_cache_path):
            with open(imgur_cache_path, "r", encoding="utf-8") as f:
                try:
                    cached_data = json.load(f)
                    if all(k in cached_data for k in ["id", "url", "deletehash"]):
                        print(f"📂 Using cached Imgur upload data from {imgur_cache_path}")
                        return {
                            "id": cached_data["id"],
                            "url": cached_data["url"],
                            "deletehash": cached_data["deletehash"],
                            "image_path": image_path  # Ensure `image_path` is included
                        }
                except json.JSONDecodeError:
                    print(f"⚠️ Corrupted .imgurUpload file. Re-uploading image...")
        
        print(f"📤 Uploading {image_path} to Imgur...")
        uploaded_image = self.client.upload_from_path(image_path, config=None, anon=True)
        print(uploaded_image)
        
                # Step 3️⃣: Save response to `.imgurUpload`
        imgur_data = {
            "id": uploaded_image["id"],
            "url": uploaded_image["link"],
            "deletehash": uploaded_image["deletehash"],
            "image_path": image_path
        }
        
        with open(imgur_cache_path, "w", encoding="utf-8") as f:
            json.dump(imgur_data, f, indent=4)

        print(f"✅ Imgur upload data saved at {imgur_cache_path}")
        return imgur_data

    def upload_from_base64(self, image_base64: str) -> dict:
        """
        Faz o upload de uma imagem fornecida como string Base64.

        :param image_base64: String contendo os dados da imagem em Base64.
        :return: Dicionário contendo id, url, e deletehash da imagem enviada.
        """
        try:
            # Decodificar Base64 para bytes
            image_data = base64.b64decode(image_base64)

            # Abrir a imagem em memória para verificar a qualidade
            image = Image.open(io.BytesIO(image_data))

            # Salvar a imagem como PNG sem compressão em um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
                image.save(temp_image.name, format="PNG", optimize=False)
                temp_image_path = temp_image.name

            # Fazer o upload usando o caminho do arquivo temporário
            return self.upload_from_path(temp_image_path)
        except:
            
            print('Erro em enviar imagem ao IMGUR')
            # Garantir que o arquivo temporário seja excluído
            #if 'temp_image_path' in locals() and os.path.exists(temp_image_path):
            #    os.remove(temp_image_path)


    def delete_image(self, deletehash: str, folder_path: str) -> bool:
        """
        Deleta uma imagem no Imgur usando o deletehash.

        :param deletehash: Código único fornecido pelo Imgur no momento do upload.
        :return: True se a imagem foi deletada com sucesso, False caso contrário.
        """
        try:
            print(f"🗑️ Attempting to delete Imgur image: {deletehash}")
            self.client.delete_image(deletehash)
            print(f"✅ Image successfully deleted from Imgur.")
            
            # Step 2️⃣: Remove the `.imgurUpload` file from the folder
            imgur_cache_path = os.path.join(folder_path, ".imgurUpload")

            if os.path.exists(imgur_cache_path):
                os.remove(imgur_cache_path)
                print(f"✅ Deleted cache file: {imgur_cache_path}")
            else:
                print(f"⚠️ No cache file found to delete: {imgur_cache_path}")
            return True
        except Exception as e:
            print(f"Erro ao deletar a imagem: {e}")
            return False
