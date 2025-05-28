from crewai_tools import SerperDevTool
from crewai import Agent, Task, Process
from datetime import datetime, timedelta

search_tool = SerperDevTool()

last_search = {}

def lasthour_cache(args, resultado):
    termo = args[0] #primeiro argumento e' o termo de busca
    agora = datetime.now()
    
    if termo in last_search:
        last_hour_search = last_search[termo]
        if agora - last_hour_search < timedelta(hours=1):
            return True
        return False
    
search_tool.cache_function = lasthour_cache

search_agent = Agent (
    role = "Agente de busca",
    goal = "Realizar busca na web de maneira eficiente",
    backstory = "Voce e' um especialista em buscas na internet de maneira rapida e eficaz",
    tools = [search_tool],
    allow_delegation= False 
)

############################################################
# ⚠️ O que está faltando para funcionar de fato:
# 1. Armazenamento do horário da última busca
# No seu lasthour_cache(), você verifica se last_search[termo] existe, mas nunca o 
# salva em lugar algum após uma busca ser realizada.
# 📌 Você precisa salvar o horário da última busca após a execução do search_tool com 
# sucesso.
# Exemplo (não presente ainda no código):
# last_search[termo] = datetime.now()
# Sem isso, o cache nunca é preenchido e o sistema sempre entende que não há cache válido.
####################################################

# defina task, crew e kickoff()    
