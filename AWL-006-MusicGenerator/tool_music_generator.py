from crewai.tools import BaseTool
from agno.tools.models_labs import ModelsLabTools, FileType
from agno.utils.log import logger
import os
import requests
from uuid import uuid4

class MusicGeneratorTool(BaseTool):
    """
    A tool for generating music using the ModelsLab API.
    """
    name: str = "Music Generator"
    description: str = "Generates music based on a provided prompt, using the ModelsLab API. Requires a ModelsLab API key."

    def __init__(self, models_lab_api_key: str):
        """
        Initializes the MusicGeneratorTool.

        Args:
            models_lab_api_key (str): The API key for accessing the ModelsLab API.
        """
        self.models_lab_api_key = models_lab_api_key
        self.models_lab_tool = ModelsLabTools(api_key=self.models_lab_api_key, wait_for_completion=True, file_type=FileType.MP3)


    def _run(self, prompt: str) -> str:
        """
        Generates music based on the given prompt.

        Args:
            prompt (str): A detailed prompt describing the desired music.

        Returns:
            str: A string containing the URL of the generated music file, or an error message.
        """
        try:
            music_generation_result = self.models_lab_tool.run(prompt)
            if music_generation_result.audio and len(music_generation_result.audio) > 0:
                url = music_generation_result.audio[0].url
                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)
                response = requests.get(url)
                filename = f"{save_dir}/music_{uuid4()}.mp3"
                with open(filename, "wb") as f:
                    f.write(response.content)

                return f"Music generated successfully!  Download the file at: {filename}"

            else:
                return "Failed to generate music. Please check your prompt and API key."
        except Exception as e:
            logger.error(f"Error during music generation: {e}")
            return f"An error occurred during music generation: {e}"