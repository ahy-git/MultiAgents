# crew_prompt_rewriter.py
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM

class PromptRewriterCrew:
    def __init__(self):
        self.llm = MyLLM.Ollama_qwen3
        self.crew = self._setup_crew()

    def _setup_crew(self):
        agent = Agent(
            role="Reformulador de Prompt",
            goal="Melhorar um prompt para que produza uma resposta válida",
            backstory="Você é especializado em corrigir prompts com base em mensagens de erro",
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description="/no_think Reescreva o seguinte prompt para corrigir os erros: {original_prompt}. Motivo do erro: {error_message}",
            expected_output="Um prompt melhorado que gere um JSON com os campos corretos.",
            agent=agent
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

    def kickoff(self, original_prompt: str, error_message: str):
        return self.crew.kickoff(inputs={
            "original_prompt": original_prompt,
            "error_message": error_message
        })