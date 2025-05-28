import os
import requests
from typing import List, Type, Dict
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

yt_apikey = os.getenv("YOUTUBE_API_KEY")


class CommentsInput(BaseModel):
    video_ids: List[str] = Field(...,
                                  description="Lista de IDs de videos do Youtube")


class CommentsTool(BaseTool):
    name: str = "Youtube Comments Extractor"
    description: str = "Extrai e filtra comentarios relevantes de videos do Youtube."
    args_schema: Type[BaseModel] = CommentsInput

    def _fetch_comments(self, video_id: str) -> List[str]:

        def is_relevant_comment(comment: str) -> bool:
            irrelevant_phrases = ["parabéns", "ótimo vídeo", "gostei muito", "excelente trabalho", "top demais"]
            return not any (phrase in comment.lower() for phrase in irrelevant_phrases)
        
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params={
            "part": "snippet",
            "videoId": video_id,
            "key": yt_apikey,
            "maxResults": 100
        }
        
        response = requests.get(url,params=params)
        if response.status_code == 200:
            comments = [
                item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                for item in response.json().get("items",[])
            ]
            return [c for c in comments if is_relevant_comment(c)]
        else:
            print(f"Erro ao buscar comentarios em {video_id}: {response.status_code} - {response.text}")
            return []
    
    def _run(self,video_ids: List[str]) -> Dict[str,List[str]]:
        comments_by_videos = {}
        for video_id in video_ids:
            filtered_comments = self._fetch_comments(video_id)
            if filtered_comments:
                comments_by_videos[video_id] = filtered_comments
        return comments_by_videos
    


# # TEST
# comments_tool = CommentsTool()
# videos = [
#     "-fPZsngNMFs",
#     "m2rG6zHoxBo",
#     "m46tZX6vceI"
# ]

# resultado = comments_tool._run(video_ids=videos)

# # 🔹 Exibir o relatório
# print("📊 Commentarios:\n", resultado)

#     # "https://www.youtube.com/watch?v=-fPZsngNMFs",
#     # "https://www.youtube.com/watch?v=m2rG6zHoxBo",
#     # "https://www.youtube.com/watch?v=m46tZX6vceI"       
        