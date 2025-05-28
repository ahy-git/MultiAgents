import os
from crewai import LLM
from config.helper import load_env

load_env()


class LLMModels:
    """
    Classe responsável por gerenciar os modelos LLM disponíveis.
    """

    def __init__(self):
        self.llm_base_url = os.getenv("OLLAMA_LOCAL", "NA")
        self.llm_docker_url = os.getenv("OLLAMA_DOCKER", "NA")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "NA")
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY", "NA")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "NA")
        self.groq_api_key = os.getenv("GROQ_API_KEY","NA")

        self.models = {
            "groqllama33vers": LLM(model="groq/llama-3.3-70b-versatile",temperature=0.9),
            "groqmixtral": LLM(model="groq/mixtral-8x7b-32768",temperature=0.9),
            "groqdeepseekqwen": LLM(model="groq/deepseek-r1-distill-qwen-32b",temperature=0.9),
            "groqdeepseekllama": LLM(model="groq/deepseek-r1-distill-llama-70b",temperature=0.9),
            "deepseek8b": LLM(model="ollama/deepseek-r1:8b", base_url=self.llm_base_url, max_tokens=2048, num_ctx=12000),
            "deepseek14b": LLM(model="ollama/deepseek-r1:14b", base_url=self.llm_base_url, max_tokens=2048, num_ctx=12000),
            "deepseek32b": LLM(model="ollama/deepseek-r1:32b", base_url=self.llm_base_url, max_tokens=2048, num_ctx=12000),
            "granite31moe": LLM(model="ollama/granite3.1-moe", base_url=self.llm_base_url),
            "granite31": LLM(model="ollama/granite3.1-dense", base_url=self.llm_base_url),
            "gemma2": LLM(model="ollama/gemma2:latest", base_url=self.llm_base_url),
            "mistral": LLM(model="ollama/mistral:latest", base_url=self.llm_base_url),
            "mixtral": LLM(model="ollama/mixtral:latest", base_url=self.llm_base_url),
            "llama33": LLM(model="ollama/llama3.3:70b-instruct-q4_K_M", base_url=self.llm_base_url),
            "llama32": LLM(model="ollama/llama3.2:latest", base_url=self.llm_base_url, max_tokens=4096, num_ctx=12000),
            "llama321b": LLM(model="ollama/llama3.2:1b", base_url=self.llm_base_url, max_tokens=4096, num_ctx=12000),
            "llama32docker": LLM(model="ollama/llama3.2:latest", base_url=self.llm_docker_url, max_tokens=2048, num_ctx=12000),
            "llama321bdocker": LLM(model="ollama/llama3.2:1b", base_url=self.llm_docker_url, max_tokens=2048, num_ctx=12000),
            "mistrallarge": LLM(model="mistral/mistral-large-latest", api_key=self.mistral_api_key),
            "mistralsmall": LLM(model="mistral/mistral-small-latest", api_key=self.mistral_api_key),
            "gpt4omini": LLM(model="openai/gpt-4o-mini", api_key=self.openai_api_key),
            "geminiflash": LLM(model="gemini/gemini-1.5-flash", api_key=self.gemini_api_key),
            "geminiflash2": LLM(model="gemini/gemini-2.0-flash-exp", api_key=self.gemini_api_key),
        }

    def get_model(self, model_name: str):
        """ Retorna o modelo especificado se disponível. """
        return self.models.get(model_name, None)

    def list_models(self):
        """ Retorna uma lista dos modelos disponíveis. """
        return list(self.models.keys())


# Instância global dos modelos LLM
llm_models = LLMModels()
