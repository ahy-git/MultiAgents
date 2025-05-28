import requests
import base64
import json


class OllamaImageDescriber:
    # Garantir que o autopost_service tenha acesso ao Ollama pela rede docker ou normal.
    def __init__(self, api_url="http://ollama:11434/api/generate", model="gemma3:latest"):
   # def __init__(self, api_url="http://localhost:11434/api/generate", model="llama3.2-vision"):     
        """
        Inicializa a classe para se comunicar com a API local do Ollama.

        Args:
            api_url (str): URL da API do Ollama.
            model (str): Nome do modelo usado para descrição de imagem.
        """
        self.api_url = api_url
        self.model = model

    def encode_image(self, image_path):
        """
        Codifica uma imagem para base64.

        Args:
            image_path (str): Caminho do arquivo da imagem.

        Returns:
            str: String base64 representando a imagem.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def describe_image(self, image_path):
        """
        Envia a imagem para a API do Ollama e obtém a descrição.

        Args:
            image_path (str): Caminho da imagem a ser descrita.

        Returns:
            str: Descrição gerada pelo Ollama.
        """
        image_base64 = self.encode_image(image_path)

        payload = {
            "model": self.model,
            "prompt": """
            You are an assistant specialized in image analysis for social media. Your task is to analyze the provided image and generate a detailed description of its content.

** Visual Description:**
1. What are the main elements in the image? (Example: landscape, people, objects, text, graphics)
2. What emotions does the image convey? (Happiness, nostalgia, energy, surprise, professionalism)
3. What is the dominant color palette in the image? (Warm tones, cool tones, pastel, vibrant colors)
4. Are there any visible logos or text in the image? If so, describe them.

**Expected Response Format:**
description": "Image of a sunset on a beach, with golden tones and a colorful sky."
"emotion": "Tranquility and inspiration" 
"color_palette": "Warm and vibrant tones 
        """,
        "images": [image_base64]
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(self.api_url, data=json.dumps(
            payload), headers=headers, stream=True)

        if response.status_code != 200:
            return f"Erro na requisição: {response.status_code}, {response.text}"

        # Processar resposta linha a linha para evitar erro de JSON
        description = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_data = json.loads(line.decode("utf-8"))
                    description += json_data.get("response", "")
                except json.JSONDecodeError:
                    continue  # Ignora linhas que não sejam JSON válidos

        return description.strip() if description else "Nenhuma descrição gerada."
