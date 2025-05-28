# app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.social_media.whatsapp_notifier import MessageFromWhatsapp, responseOkToWhatsapp
from core.image_processing.image_decode_save import ImageDecodeSaver
from core.image_processing.applyBorder import ImageWithBorder
from core.image_processing.filterImage import FilterImage
from infra.imgur.imgur_service import ImageUploader
from core.ai.describe_image import ImageDescriber
from core.ai.generate_caption import InstagramPostCrew
from core.social_media.instagram_post import InstagramPostService



from flask import Flask, request

app = Flask(__name__)

border_image = "moldura.png"


@app.route("/messages-upsert", methods=['POST'])
def webhook():
    
    data = request.get_json()  
    
    print(data)
            
    msg = MessageFromWhatsapp(data)
    texto = msg.get_text()
    
    send = responseOkToWhatsapp()

    if msg.scope == MessageFromWhatsapp.SCOPE_GROUP:    
        
        print(f"Grupo: {msg.group_id}")
        
        if str(msg.group_id) == "120363372879654391":
             
            if msg.message_type == msg.TYPE_IMAGE:
                
                image_path = ImageDecodeSaver.process(msg.image_base64)
                
                image_path = FilterImage.process(image_path)
                
                image = ImageUploader().upload_from_path(image_path)
                
                describe = ImageDescriber.describe(image['url'])
                
                ImageUploader().delete_image(image["deletehash"])
                
                image = ImageWithBorder.create_bordered_image(
                    border_path=border_image,
                    image_path=image_path,
                    output_path=image_path                
                )
                
                image = ImageUploader().upload_from_path(image_path)
                
                crew = InstagramPostCrew()
                caption = crew.kickoff(inputs={"caption": texto,
                                            "describe": describe,
                                            "estilo": "Divertido, Alegre, descontraído, linguagem simples",
                                            "pessoa": "Terceira pessoa do singular",
                                            "sentimento": "Positivo",
                                            "tamanho":"200 palavras",
                                            "genero":"Indefinido",
                                            "emojs":"sim",
                                            "girias":"nao"
                                            })
                
                
                caption = caption + "\n\n-------------------"
                caption = caption + "\n\n Essa postagem foi toda realizada por um agente inteligente"
                caption = caption + "\n O agente desempenhou as seguintes ações:"
                caption = caption + "\n 1 - Idenficação e reconhecimento do ambiente da fotografia"
                caption = caption + "\n 2 - Aplicação de Filtros de contraste e autocorreção da imagem"
                caption = caption + "\n 3 - Aplicação de moldura azul específica"
                caption = caption + "\n 4 - Definição de uma persona divertida, Alegre, Sarcástica e descontraída"
                caption = caption + "\n 5 - Criação da legenda com base na imagem e na persona"
                caption = caption + "\n 6 - Postagem no feed do instagram"
                caption = caption + "\n 7 - Técnica ensinada no livro Agentes Inteligentes 2 - CrewAI Intermediário"
                
                
                
                insta_post = InstagramPostService()
                insta_post.post_image(image['url'], caption)
                
                send = responseOkToWhatsapp()
                send.send_message(msg.group_id, "Postagem realizada com sucesso.")
                
                #APAGANDO IMAGENS
                ImageUploader().delete_image(image["deletehash"])
                # Verificar se o arquivo existe e apagar
                if os.path.exists(image['image_path']):
                    os.remove(image['image_path'])
                    print(f"A imagem {image['image_path']} foi apagada com sucesso.")
                
            
    return "" 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

