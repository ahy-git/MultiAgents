import os
from openai import OpenAI
from dotenv import load_dotenv

class ImageDescriber:
    
    @staticmethod
    def describe(image_url: str) -> str:
        """
        Gera uma descrição detalhada para a imagem fornecida.

        Args:
            image_url (str): URL da imagem a ser analisada.

        Returns:
            str: Descrição gerada para a imagem.
        """
        load_dotenv()  # Carregar variáveis de ambiente do arquivo .env

        # Configurar o cliente OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Fazer a solicitação à API da OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Substitua pelo modelo correto, caso necessário
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                                Me dê uma ideia do contexto do ambiente da imagem e do que está ocorrendo na imagem.
                                Quais são as expressões faciais predominantes (feliz, triste, neutro, etc.)?                                
                                Qual é a expressão emocional delas? 
                                Além disso, descreva qualquer objeto ou elemento marcante na cena.
                                Tente identificar se é dia ou noite, ambiente aberto ou fechado,
                                de festa ou calmo. O que as pessoas estão fazendo?
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        # Extraindo a descrição da resposta
        try:
            description = response.choices[0].message.content
            return description.strip()
        except (KeyError, IndexError) as e:
            return f"Erro ao processar a descrição da imagem: {e}"


