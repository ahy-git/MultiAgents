import os
import requests
from typing import List, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from model_youtube_video import YouTubeVideo

load_dotenv()

yt_apikey = os.getenv("YOUTUBE_API_KEY")

class VideoDetailsInput(BaseModel):
    """
        Schema para entrada da ferramenta de extracao
    """
    video_ids: List[str] = Field(...,description="Lista de IDs de videos para analise")

class YouTubeVideoTool(BaseTool):
    name: str = "Youtube Video Details Extractor"
    description: str ="Busca informacoes detalhadas de uma lista de videos do youtube"
    args_schema: Type[BaseModel] = VideoDetailsInput
    
    def _fetch_video_details(self,video_id:str) -> YouTubeVideo:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": video_id,
            "key": yt_apikey,
        }
        
        response = requests.get(url,params=params)
        if response.status_code ==200:
            video_data = response.json().get("items",[])
            if video_data:
                return YouTubeVideo.from_api_response(video_data)[0]
            else:
                print(f"Erro na requisicao video {video_id}: {response.status_code} - {response.text}")
            
            return None
    
    def _run(self,video_ids: List[str]) -> List[YouTubeVideo]:
        """
        Obtem detalhes de uma lista de videos
        """
        videos = []
        for video_id in video_ids:
            video_info = self._fetch_video_details(video_id)
            if video_info:
                videos.append(video_info)
        
        return videos       
