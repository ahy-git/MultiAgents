import os
import requests
from uuid import uuid4
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

class ElevenLabsTool(BaseTool):
    name :str = "ElevenLabs Audio Generator"
    description : str = "Gera áudio a partir de texto com voz natural usando a ElevenLabs API."

    def _run(self, text: str) -> str:
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY não está definida no ambiente.")

        voice_id = "JBFqnCBsd6RMkjVDRZzb"
        model_id = "eleven_multilingual_v2"
        output_dir = "audio_generations"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"podcast_{uuid4()}.wav")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Erro ElevenLabs: {response.status_code} - {response.text}")

        with open(output_path, "wb") as f:
            f.write(response.content)

        return output_path



# texto = (
#     "Olá! Este é um exemplo de geração de voz com a ElevenLabs usando a integração via CrewAI."
# )

# tool = ElevenLabsTool()
# try:
#     audio_file = tool.run(texto)
#     print(f"\n🟢 Áudio salvo em: {audio_file}")
# except Exception as e:
#     print(f"\n🔴 Erro: {e}")