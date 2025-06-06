from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM
from GmailReader import GmailReaderTool
import re

class EmailTriageCrew:
    def __init__(self):
        self.llm = MyLLM.Ollama_qwen3_14b
        self.crew = self._setup_crew()

    def _setup_crew(self):
        reader_tool = GmailReaderTool()

        agent = Agent(
            role="Analista de Caixa de Entrada",
            goal="Ler e classificar os e-mails recebidos como importantes ou não.",
            backstory="Você ajuda seu usuário a manter o foco apenas nos e-mails essenciais.",
            tools=[reader_tool],
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description="""Use a ferramenta para ler os e-mails e 
            classifique os que exigem atenção urgente. Retorne um resumo com título,
            remetente e por que é importante. Ignore se o email e' spam ou propaganda.
            Foque e analise um email real, realmente direcionado a mim ou fatura, boleto, comunicado, ou direcionado. 
            Leia todo o conteudo e faca essa analise critica""",
            expected_output="""
            Lista dos e-mails importantes com título e justificativa.
            Escreva um breve resumo e as acoes a serem tomadas.
            """,
            agent=agent
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

    def kickoff(self):
        return self.crew.kickoff()
    
    
if __name__ == "__main__":
    crew = EmailTriageCrew()
    result = crew.kickoff()
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()
    print(result)
