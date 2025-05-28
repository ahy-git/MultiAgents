from crewai import Agent,Task,Crew,Process
from tool_youtube_videos import YouTubeVideoTool
from MyLLM import MyLLM

class YouTubeVideoAnalyzer:
    
    def __init__(self):
        self.llm = MyLLM.geminiflash15
        self.crew = self._setup_crew()
    
    def _setup_crew(self):
        agent_analista_videos = Agent(
            role=r"""Analista de Vídeos do YouTube""",
            goal=r"""Analisar uma lista de vídeos do YouTube e gerar insights detalhados sobre engajamento e tendências.""",
            backstory=r"""
                Você é um especialista em análise de vídeos do YouTube. Seu objetivo é revisar métricas como 
                visualizações, curtidas e comentários para entender padrões de engajamento e prever tendências futuras.
            """,
            tools=[YouTubeVideoTool()],  # Agora usamos a nova ferramenta
            verbose=True                 
        )
        
        task_analise_videos = Task(
            description=r"""
                Analise a seguinte lista de vídeos do YouTube:
                
                {video_ids}
                
                Para cada vídeo, colete as seguintes informações:
                - Título do vídeo
                - Canal
                - Número de visualizações
                - Curtidas
                - Comentários
                - Duração do vídeo
                - Se tem legendas disponíveis
                
                A partir desses dados, gere um relatório sobre padrões de engajamento e possíveis tendências emergentes.
            """,
            expected_output=r"""
                Um relatório detalhado analisando os vídeos fornecidos, destacando padrões de engajamento, 
                crescimento e previsões sobre tendências futuras.
            """,
            agent=agent_analista_videos            
            
        )
        
        return Crew(
            agents=[agent_analista_videos],
            tasks=[task_analise_videos],
            process=Process.sequential  # O agente executa a tarefa de forma sequencial            
        )

    def kickoff(self,video_links):
        
        video_ids = [link.split('v=')[-1] for link in video_links]
        inputs = {"video_ids": "\n".join(video_ids)}
        print(f"[TOOL] Coletando dados dos vídeos: {video_ids}")
        ret = self.crew.kickoff(inputs= inputs)
        return ret.raw

## TEST
# video_analyzer = YouTubeVideoAnalyzer()
# videos = [
#     "https://www.youtube.com/watch?v=-fPZsngNMFs",
#     "https://www.youtube.com/watch?v=m2rG6zHoxBo",
#     "https://www.youtube.com/watch?v=m46tZX6vceI"
# ]

# resultado = video_analyzer.kickoff(video_links=videos)

# # 🔹 Exibir o relatório
# print("📊 Análise dos vídeos fornecidos:\n", resultado)       
        
        
        