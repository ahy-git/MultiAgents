import os
from dotenv import load_dotenv
from evolutionapi.client import EvolutionClient
from evolutionapi.models.message import TextMessage, MediaMessage

class SendWhatsapp:
    def __init__(self) -> None:
        load_dotenv()
        self.evo_api_token = os.getenv('EVO_API_TOKEN')
        self.evo_instance_id = os.getenv('EVO_INSTANCE_NAME')
        self.evo_instance_token= os.getenv('EVO_INSTANCE_TOKEN')
        self.evo_base_url = os.getenv('EVO_BASE_URL')
        
        self.client = EvolutionClient(
            base_url = self.evo_base_url,
            api_token= self.evo_api_token
        )
        
    def textMessage(self, number, msg, mentions=[]):
        
        text_message = TextMessage(
            number=number,
            text=msg,
            mentioned=mentions
        )
        
        response = self.client.messages.send_text(
            self.evo_instance_id,
            text_message,
            self.evo_instance_token
        )
        
        return response
    
    def PDF(self,number,pdf_file, caption=""):
        
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"File {pdf_file} not found")
        
        media_message = MediaMessage(
            number=number,
            mediatype="document",
            mimetype = "application/pdf",
            caption=caption,
            fileName=os.path.basename(pdf_file),
            media=""            
        )
        
        response = self.client.messages.send_media(
            self.evo_instance_id,
            media_message,
            self.evo_instance_token,
            pdf_file
        )
        
        return "PDF enviado"
    
    def audio(self,number,audio_file):
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"File {audio_file} not found")
    
        audio_message ={
            "number" : number,
            "mediatype" : "audio",
            "mimetype" : "audio/mpeg",
            "caption" : ""
        }
        
        response = self.client.messages.send_whatsapp_audio(
            self.evo_instance_id,
            audio_message,
            self.evo_instance_token,
            audio_file
        )
        
        return "Audio enviado"

    def image(self,number,image_file,caption=""):
        if not os.path.exists(image_file):
            raise FileNotFoundError(f"File {image_file} not found")            
    
        media_message = MediaMessage(
            number=number,
            mediatype="image",
            mimetype="image/jpeg",
            caption=caption,
            fileName=os.path.basename(image_file),
            media=""            
        )
        
        response = self.client.messages.send_media(
            self.evo_instance_id,
            media_message,
            self.evo_instance_token,
            image_file
        )
        
        return 'Imagem enviada'
    
    def video (self, number, video_file, caption=""):
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"File {video_file} not found") 
        
        media_message = MediaMessage(
            number=number,
            mediatype="video",
            mimetype="video/mp4",
            caption=caption,
            fileName=os.path.basename(video_file),
            media=""
        )           
        
        response = self.client.messages.send_media(
            self.evo_instance_id,
            media_message,
            self.evo_instance_token,
            video_file
        )
        
        return "Video enviado"
    
    def document(self, number, document_file, caption=""):
        if not os.path.exists(document_file):
            raise FileNotFoundError(f"File {document_file} not found")
        
        media_message = MediaMessage(
            number=number,
            mediatype="document",
            mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            caption=caption,
            fileName=os.path.basename(document_file),
            media=""            
        )
        
        self.client.messages.send_media(
            self.evo_instance_id,
            media_message,
            self.evo_instance_token,
            document_file,
        )                 
        
        return "Documento enviado"
    
             