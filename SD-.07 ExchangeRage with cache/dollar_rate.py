from crewai.tools import tool
from datetime  import datetime, timedelta
import requests
from crewai import Agent, Task, Crew
from MyLLM import MyLLM

llm = MyLLM.geminiflash15

ultima_consulta = None

@tool
def ferramenta_cotacao_dolar() -> str:
    "Consulta da taxa do dolar referente ao real"
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        cotacao_dolar = dados["USDBRL"]["bid"]
        return f'Dolar vale R$ {cotacao_dolar}'
    else:
        return "Erro ao consultar cotacao do dolar"
    
def funcao_cache (argumentos, resultado):
    global ultima_consulta
    agora = datetime.now()
    
    if ultima_consulta and ( agora - ultima_consulta < timedelta(hours=1)):
        return True
    else:
        ultima_consulta = agora
        return False

ferramenta_cotacao_dolar.cache_function = funcao_cache

exchange_agent = Agent(
    role="Agente de Cambio",
    goal="Monitorar a cotacao do dolar ao longo do dia",
    backstory="Voce e' responsavel por consultar e reportar a cotacao do dolar sobre o real",
    tools = [ferramenta_cotacao_dolar],
    llm = llm,
    allow_delegation=False
)

exchange_rate_task = Task(
    description='Verifica a cotacao do dolar',
    agent = exchange_agent,
    expected_output="a cotacao do dolar relativa ao real com R$ . Deve-se informar se usou cache ou nao",
    tool=[ferramenta_cotacao_dolar]
)

exchange_rate_crew = Crew(
    agents=[exchange_agent],
    tasks=[exchange_rate_task]
)

results = exchange_rate_crew.kickoff()

print(results)
