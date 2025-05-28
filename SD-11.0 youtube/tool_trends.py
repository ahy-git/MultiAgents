import os
import requests
from typing import Type, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from model_youtube_video import YouTubeVideo

load_dotenv()

yt_apikey = os.getenv("YOUTUBE_API_KEY")

class TrendInput(BaseModel):
    category: str = Field(...,description="ID categoria do Youtube")
    region: str = Field(...,description="Codigo da Regiao (ex: BR, US)")
    max_results: int = Field(5,description="Numero maximo de videos a buscar")
    num_comments: int = Field(10,description="Numero maximo de comentarios a buscar")
    
class TrendTool(BaseTool):
    name: str = "Youtube trends Finder"
    description: str = "Busca videos populares no Youtube com base em categorias e regiao e coleta informacoes relevantes"
    args_schema: Type[BaseModel] = TrendInput
    last_results: List[YouTubeVideo] = []
    
    def _fetch_comments(self, video_id: str, num_comments: int) -> List[str]:
        """Busca os primeiros comentários de um vídeo, ajustando a quantidade conforme solicitado."""
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": num_comments,
            "textFormat": "plainText",
            "key": yt_apikey,
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            comments = response.json().get("items", [])
            return [comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for comment in comments]
        return ["Nenhum comentário disponível."]
    
    def _run(
        self,
        category: str ="28",
        region: str = "BR",
        max_results: int = 5,
        num_comments: int = 10             
             ) -> str:
        
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics,contentDetails",
            "chart": "mostPopular",
            "regionCode": region,
            "videoCategoryId": category,
            "maxResults": max_results,
            "key": yt_apikey,
        }

        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            videos = response.json().get("items",[])
            self.last_results = YouTubeVideo.from_api_response(videos)

            for video in self.last_results:
                video.top_comments = self._fetch_comments(video_id=video.videoId, num_comments=num_comments)
            return self._generate_report
        else:
            raise ValueError(f"Erro na requisicao: {response.status_code} - {response.text}")
        
    def _generate_report(self) -> str:
        
        if not self.last_results:
            return "Nenhuma tendencia encontrada"
        
        return "\n\n".join(str(video) for video in self.last_results)


## TEST
# trend = TrendTool()
# resultado = trend._run()  # Vai buscar tendências de Tecnologia no Brasil com 10 comentários
# print(resultado)  # Exibe o relatório gerado
            
        
    