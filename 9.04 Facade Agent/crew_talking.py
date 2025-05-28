from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM

class TalkingCrew:
    def __init__(self, verbose=True, memory=True):
        self.llm=MyLLM.geminiflash20
        
        self.agent = Agent(
            role = "Processador de transcricoes",
            goal = "Receber uma transcricao de audio como texto e produzir uma respostsa relevante e coerente",
            backstory = "Especialista em compreender contextos e responder com clareza",
            memory = True,
            verbose=verbose,
            llm=self.llm
        )
        
        self.task= Task(
            description =(
                "Analise texto dentro de <texto>, forneca uma resposta ou faca um comentario: "
                "<texto>{transcription_text}</texto>. A resposta ser clara e objetiva. Recomendar e sugerir sao boas praticas. SEMPRE RESPONDA EM PT-BR"
            ),
            expected_output="Um texto com uma resposta coerente e relevante",
            agent=self.agent
        )
        
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential
        )

    def kickoff(self,transcription):
        
        result = self.crew.kickoff(inputs={"transcription_text" : transcription})
        return result.raw
    
           