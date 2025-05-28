from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()

class MyLLM():
    # Modelos OpenAI
    gpt_mini                = LLM(model="gpt-4o-mini")
    gpt4o_mini              = LLM(model="gpt-4o-mini")
    gpt4o_mini_2024_07_18   = LLM(model="gpt-4o-mini-2024-07-18")
    gpt_4o_2024_08_06       = LLM(model="gpt-4o-2024-08-06")
    gpt4o                   = LLM(model="gpt-4o")
    gpt_o1                  = LLM(model="o1-preview")
    gpt_o1_mini             = LLM(model="o1-mini")

    # Modelos Ollama (executados localmente)
    Ollama_llama_3_1        = LLM(model="ollama/llama3.1", base_url="http://localhost:1140/openai-8B")
    Ollama_deepseek_14b     = LLM(model="ollama/deepseek-r1:14b", base_url="http://localhost:11434")

    # Modelos Groq
    groq_llama3_70b         = LLM(model="groq/llama-3.3-70b-versatile")
    groq_llama3_8b          = LLM(model="groq/llama-guard-3-8b")
    groq_mixtral            = LLM(model="groq/mixtral-8x7b-32768")
    groq_deepseek_70b       = LLM(model="groq/deepseek-r1-distill-llama-70b")
    groq_gemma2_9b          = LLM(model="groq/gemma2-9b-it")
    
    # Modelo Gemini
    geminiflash15=  LLM(model="gemini/gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
    geminiflash20=  LLM(model="gemini/gemini-2.0-flash-exp", api_key=os.getenv("GEMINI_API_KEY"))
   
    # Modelos OpenRouter
    openrouter_llama_3_1_405b = LLM(model="openrouter/meta-llama/llama-3.1-405b-instruct:free", base_url="https://openrouter.ai/api/v1")
    openrouter_deepseek_r1    = LLM(model="openrouter/deepseek/deepseek-r1:free", base_url="https://openrouter.ai/api/v1")