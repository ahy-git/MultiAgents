from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()
OLLAMA_BASE_URL = "http://localhost:11434"

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
    Ollama_llama_3_2        = LLM(model="ollama/llama3.2:latest", base_url=OLLAMA_BASE_URL,max_tokens=4096,max_completion_tokens=2048,timeout=1200)
    Ollama_deepseek_14b     = LLM(model="ollama/deepseek-r1:14b", base_url=OLLAMA_BASE_URL,max_tokens=4096,max_completion_tokens=2048,timeout=1200)
    Ollama_qwen3            = LLM(model="ollama/qwen3:8b",base_url=OLLAMA_BASE_URL,max_tokens=131072,timeout=1200)
    Ollama_gemma3           = LLM(model="ollama/gemma3:latest",base_url=OLLAMA_BASE_URL,max_tokens=4096, max_completion_tokens=2048,timeout=1200)
    ollama_mistral          = LLM(model="ollama/mistral:latest",base_url=OLLAMA_BASE_URL,max_tokens=4096, max_completion_tokens=2048,timeout=1200)          
    Ollama_qwen3_14b        = LLM(model="ollama/qwen3:14b",base_url=OLLAMA_BASE_URL,max_tokens=131072,timeout=1200)


    
    #Mistral
    mistral_large           =  LLM(model="mistral/mistral-large-latest", api_key=os.getenv("MISTRAL_API_KEY"))
    mistral_small           =  LLM(model="mistral/mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY"))
    
    
    # Modelos Groq
    groq_llama3_70b         = LLM(model="groq/llama-3.3-70b-versatile")
    groq_llama3_8b          = LLM(model="groq/llama-guard-3-8b")
    groq_mixtral            = LLM(model="groq/mixtral-8x7b-32768")
    groq_deepseek_70b       = LLM(model="groq/deepseek-r1-distill-llama-70b")
    groq_gemma2_9b          = LLM(model="groq/gemma2-9b-it")
    
    # Modelo Gemini
    geminiflash15=  LLM(model="gemini/gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
    geminiflash20=  LLM(model="gemini/gemini-2.0-flash-lite", api_key=os.getenv("GEMINI_API_KEY"))
   
    # Modelos OpenRouter
    openrouter_llama_3_1_405b = LLM(model="openrouter/meta-llama/llama-3.1-405b-instruct:free", base_url="https://openrouter.ai/api/v1")
    openrouter_deepseek_r1    = LLM(model="openrouter/deepseek/deepseek-r1:free", base_url="https://openrouter.ai/api/v1")