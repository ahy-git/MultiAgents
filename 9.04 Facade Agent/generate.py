import os
import requests
from dotenv import load_dotenv

class TextToSpeech:
    def __init__(self, chunk_size=1024):
        """Inicializa classe TextToSpeech com chunk para download

        Args:
            chunk_size (int, optional): Tamanho do chunk para download do audio. Defaults to 1024.
        """
        load_dotenv()
        self.api_key=os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = "EIkHVdkuarjkYUyMnoes"
        self.chunk_size = 1024
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"
        
        self.data_template = {
            "model_id" : "eleven_turbo_v2_5",
            "voice_settings" : {
                "stability" : 0.2,
                "similarity_boost" : 1,
                "speed" : 1.2
            }
        }
        
        self.headers = {
            "Accept" : "audio/mpeg",
            "Content-type" : "application/json",
            "xi-api-key" : self.api_key
        }
    
    def synthesize_speech(self, text, output_file):
        """Gera um audio a partir de um texto usando eleven labs

        Args:
            text (_type_): texto a ser convertido
            output_file (_type_): arquivo de audio
        """
    
        url = f"{self.base_url}/{self.voice_id}"
        
        data = self.data_template.copy()
        data["text"] = text
        
        response = requests.post(url,json=data, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Erro na requisicao: {response.status_code} - {response.text}")
        
        with open(output_file,"wb") as f: 
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    f.write(chunk)
        print(f"Audio gerado com sucesso em {output_file}")
