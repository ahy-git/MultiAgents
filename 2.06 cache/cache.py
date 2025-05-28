from crewai.tools import tool
from crewai import Agent

@tool 
def multiplicationTool(primeiro_numero: int, 
                       segundo_numero:int) -> str:
    "Multiplicador simples de dois inteiros"
    
def cache_func(args, result):
    cache = result % 2 == 0
    return cache

multiplicationTool.cache_function = cache_func

writer = Agent(
    role = "Escritor",
    goal = "Voce escreve licoes de matematica para criancas",
    backstory = "Voce eh um especialista em redacao e adora ensina criancas mas nao sabe nada de matematica",
    tools = [multiplicationTool],
    allow_delegation= False
)
