import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FirecrawlScrapeWebsiteTool
from dotenv import load_dotenv
from MyLLM import MyLLM
from toolElevenLabs import ElevenLabsTool

load_dotenv()


class BlogToPodcastCrew:
    def __init__(self):
        self.llm = MyLLM.gpt4o_mini
        self.elevenLabsTool = ElevenLabsTool()
        self.fireCrawlTool = FirecrawlScrapeWebsiteTool()
        self.crew = self._setup_crew()

    def _setup_crew(self):
        agent = Agent(
            role="Narrador de Podcast",
            goal="Transformar conteúdo de blog em podcast com até 2000 caracteres",
            backstory=(
                "Você é um agente que resume artigos de blog de forma envolvente e converte o conteúdo em áudio "
                "natural com voz humana por meio da API da ElevenLabs."
            ),
            tools=[self.elevenLabsTool, self.fireCrawlTool],
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description=(
                "1. Use a ferramenta FirecrawlScrapeWebsiteTool para acessar o conteúdo da URL: {url}.\n"
                "Exemplo: {'url': 'https://exemplo.com'}. Não passe mais de um argumento.\n"
                "Depois, gere um resumo com até 2000 caracteres e converta para áudio com ElevenLabsTool.\n"
                "2. Resuma o conteúdo em até 2000 caracteres com linguagem natural e envolvente.\n"
                "3. Gere um áudio com esse resumo usando ElevenLabsTool.\n"
                "Retorne apenas o caminho do arquivo gerado."
            ),
            expected_output="Caminho do arquivo .wav gerado com a narração do blog.",
            agent=agent
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

    def kickoff(self, url: str) -> str:
        try:
            result = self.crew.kickoff(inputs={"url": url})
            audio_path = self._extract_audio_file()
            return audio_path
        except Exception as e:
            print(f"Erro durante geração do podcast: {e}")
            raise

    def _extract_audio_file(self, save_dir: str = "audio_generations") -> str:
        os.makedirs(save_dir, exist_ok=True)
        files = sorted(
            [f for f in os.listdir(save_dir) if f.endswith(".wav")],
            key=lambda x: os.path.getmtime(os.path.join(save_dir, x)),
            reverse=True
        )
        if not files:
            raise RuntimeError("Nenhum arquivo de áudio encontrado.")
        return os.path.join(save_dir, files[0])


# Execução direta
if __name__ == "__main__":
    crew = BlogToPodcastCrew()
    podcast_file = crew.kickoff("https://firecrawl.dev")
    print(f"✅ Podcast salvo em: {podcast_file}")
