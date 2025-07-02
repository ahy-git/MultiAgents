from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM  # Assuming MyLLM handles the LLM interaction (like OpenAI)
from tool_music_generator import MusicGeneratorTool
import os

class MusicGenerationCrew:
    """
    A CrewAI crew for generating music based on user prompts.
    """
    def __init__(self, openai_api_key: str, models_lab_api_key: str):
        """
        Initializes the MusicGenerationCrew.

        Args:
            openai_api_key (str): The API key for OpenAI.
            models_lab_api_key (str): The API key for ModelsLab.
        """
        self.llm = MyLLM.Ollama_qwen3_14b  # Or however MyLLM is initialized.
        self.openai_api_key = openai_api_key
        self.models_lab_api_key = models_lab_api_key
        self.crew = self._setup_crew()

    def _setup_crew(self):
        """
        Sets up the CrewAI crew with an agent and a task.
        """
        music_generator_tool = MusicGeneratorTool(models_lab_api_key=self.models_lab_api_key)

        music_agent = Agent(
            role="Music Composer",
            goal="Compose high-quality music based on user prompts, using the ModelsLab API.",
            backstory="You are a creative music composer specializing in various genres.",
            tools=[music_generator_tool],
            llm=self.llm,
            verbose=True
        )

        music_task = Task(
            description="Compose a piece of music based on the following prompt: <prompt>. Be specific about the genre, style, instruments, and any other relevant details. The output should be a downloadable link to the mp3 file.",
            agent=music_agent,
            expected_output="A downloadable link to the generated music file.",
        )

        return Crew(
            agents=[music_agent],
            tasks=[music_task],
            process=Process.sequential,
        )

    def kickoff(self, prompt: str):
        """
        Kicks off the music generation process.

        Args:
            prompt (str): The prompt for generating music.

        Returns:
            str: The result of the music generation process.
        """
        music_task = self.crew.tasks[0]
        music_task.description = music_task.description.replace("<prompt>", prompt)
        return self.crew.kickoff()

if __name__ == "__main__":
    # Example usage (replace with your actual keys and prompt)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    models_lab_api_key = os.getenv("MODELS_LAB_API_KEY")

    if not openai_api_key or not models_lab_api_key:
        print("Please set your OPENAI_API_KEY and MODELS_LAB_API_KEY environment variables.")
    else:
        prompt = "Compose a 30-second upbeat jazz music piece with a saxophone solo."
        crew = MusicGenerationCrew(openai_api_key=openai_api_key, models_lab_api_key=models_lab_api_key)
        result = crew.kickoff(prompt)
        print(result)