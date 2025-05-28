import os
from dotenv import load_dotenv
from evolutionapi.client import EvolutionClient
from evolutionapi.models.message import TextMessage, MediaMessage

load_dotenv()

evo_api_token = os.getenv('EVO_API_TOKEN')
evo_instance_id = os.getenv('EVO_INSTANCE_NAME')
evo_instance_token= os.getenv('EVO_INSTANCE_TOKEN')
evo_base_url = os.getenv('EVO_BASE_URL')

client = EvolutionClient(
    base_url = evo_base_url,
    api_token=evo_api_token
)

text_message = TextMessage(
    number='5511984617987',
    text='Teste do evolution com python'
)

response = client.messages.send_text(evo_instance_id,text_message,evo_instance_token)

print(response)