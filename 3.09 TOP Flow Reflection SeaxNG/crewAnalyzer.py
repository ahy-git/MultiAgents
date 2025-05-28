from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv


load_dotenv()

class crewAnalyzer:
    def __init__(self):
        self.llm = 'gemini/gemini-2.0-flash-lite'
        self.crew = self._criarcrew()
    
    def _criarcrew(self):
        analisador = Agent(
            role='Analisador',
            goal = 'Criticar e sugerir melhorias em um texto proposto',
            verbose=True,
            llm=self.llm,
            backstory ="""
            Você é um analisador experiente , especializado em
            identificar pontos fracos em textos 
            e sugerir melhorias para torn á-los mais claros ,
            envolventes e impactantes . Caso o texto já
            esteja ótimo , você deve responder com " perfeito ". 
            """   
        )
        
        analise_task = Task (
            description = """
            Avalie o seguinte texto com base nos parâmetros
            fornecidos :\n\n
            - ** Tópico **: "{topic}"\n
            - ** Texto atual **: "{ideia}"\n
            - ** Crítica anterior **: "{critica}"\n\n
            - ** Objetivo do texto **: "{objetivo}"\n\n
            Forneça críticas construtivas para melhorar o texto
            considerando o tópico e o histórico 
            das críticas . Se o texto já está ótimo , diga apenas 
            "perfeito".
            """,
            expected_output="""Uma crítica detalhada do texto , 
            com sugestões de melhoria , ou "perfeito". """,
            agent = analisador
        )
        
        return Crew(
            agents=[analisador],
            tasks = [analise_task],
            process = Process.sequential
        )
        
    def kickoff(self, inputs):
        """
        Executa o Crew com os parâmetros fornecidos .
        inputs :
         - topic : str , o tópico principal do texto .
         - ideia : str , a ideia ou vers ão atual do texto .
         - critica : str , a ú ltima crítica feita ao texto .
        Returns :
         - A crí tica detalhada ou "perfeit " se o texto já está excelente
        """
        resposta = self.crew.kickoff(inputs=inputs)
        
        return resposta.raw