# crew_profile_generator.py
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM

class ProfileGeneratorCrew:
    def __init__(self):
        self.llm = MyLLM.Ollama_llama_3_2
        self.crew = self._setup_crew()

    def _setup_crew(self):
        agent = Agent(
            role="Gerador de Perfis",
            goal="Gerar um perfil em JSON com nome, idade e profissão.",
            backstory="Você é um gerador preciso de perfis estruturados.",
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description="{message}",
            expected_output="Um JSON válido com os campos exigidos.",
            agent=agent
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

    def kickoff(self, prompt: str):
        return self.crew.kickoff(inputs={"message": prompt})



