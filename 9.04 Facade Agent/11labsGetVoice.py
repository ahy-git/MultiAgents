import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

headers = {
    "xi-api-key": api_key
}

response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)

if response.status_code == 200:
    print("Vozes disponíveis para sua conta:")
    for voice in response.json().get("voices", []):
        print(f"- Nome: {voice['name']} | ID: {voice['voice_id']}")
else:
    print(f"Erro ao buscar vozes: {response.status_code} - {response.text}")
