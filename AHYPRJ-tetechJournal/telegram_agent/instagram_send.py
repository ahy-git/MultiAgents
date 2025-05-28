# import os

# from instagram.crew_post_instagram import InstagramPostCrew
# from instagram.describe_image_tool import ImageDescriber
# from instagram.instagram_post_service import InstagramPostService
# from instagram.border import ImageWithBorder

# from instagram.filter import FilterImage
# from paths import Paths

# from instagram.image_uploader import ImageUploader

# class InstagramSend:
    
    
#     @staticmethod
#     def send_instagram(image_path, caption):
        
#         border_image = os.path.join(Paths.ROOT_DIR,"instagram","moldura.png")
        
#         image_path = FilterImage.process(image_path)
        
#         image = ImageUploader().upload_from_path(image_path)
        
#         describe = ImageDescriber.describe(image['url'])
        
#         ImageUploader().delete_image(image["deletehash"])
        
#         image = ImageWithBorder.create_bordered_image(
#             border_path=border_image,
#             image_path=image_path,
#             output_path=image_path                
#         )
        
#         image = ImageUploader().upload_from_path(image_path)
        
#         crew = InstagramPostCrew()
#         caption = crew.kickoff(inputs={"caption": caption,
#                                     "describe": describe,
#                                     "estilo": "Divertido, Alegre, Sarcástico e descontraído",
#                                     "pessoa": "Terceira pessoa do singular",
#                                     "sentimento": "Positivo",
#                                     "tamanho":"200 palavras",
#                                     "genero":"Masculino",
#                                     "emojs":"sim",
#                                     "girias":"sim"
#                                     })
        
        
#         caption = caption + "\n\n-------------------"
#         caption = caption + "\n\n Essa postagem foi toda realizada por um agente inteligente"
#         caption = caption + "\n O agente desempenhou as seguintes ações:"
#         caption = caption + "\n 1 - Idenficação e reconhecimento do ambiente da fotografia"
#         caption = caption + "\n 2 - Aplicação de Filtros de contraste e autocorreção da imagem"
#         caption = caption + "\n 3 - Aplicação de moldura azul específica"
#         caption = caption + "\n 4 - Definição de uma persona divertida, Alegre, Sarcástica e descontraída"
#         caption = caption + "\n 5 - Criação da legenda com base na imagem e na persona"
#         caption = caption + "\n 6 - Postagem no feed do instagram"
#         caption = caption + "\n 7 - Técnica ensinada no livro Agentes Inteligentes 2 - CrewAI Intermediário"
        
#         insta_post = InstagramPostService()
#         insta_post.post_image(image['url'], caption)
        
#         #APAGANDO IMAGENS
#         ImageUploader().delete_image(image["deletehash"])
#         # Verificar se o arquivo existe e apagar
#         if os.path.exists(image['image_path']):
#             os.remove(image['image_path'])
#             print(f"A imagem {image['image_path']} foi apagada com sucesso.")
        
        