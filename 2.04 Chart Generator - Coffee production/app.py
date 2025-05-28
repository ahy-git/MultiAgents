from dotenv import load_dotenv
from MyLLM import MyLLM
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from graph_tool import CustomGraphTool

load_dotenv()

llm = MyLLM.gpt4o_mini

serper_tool = SerperDevTool()
serper_tool.n_results = 10
chart_tool = CustomGraphTool()

research_agent = Agent(
    role= """ Pesquisador de cafe
    """, 
    goal="""  Pesquisara producao de cafe no Brasil em 2024 por
tipo de cafe , incluindo porcentagens
    """, 
    backstory=""" Especialista em pesquisas de dados de agricultura com foco em cafe
    """,
    llm=llm,
    verbose=True, 
    allow_delegation=False,
    tools=[serper_tool]
)

chart_agent = Agent(
    role="""Criador de Graficos
    """, 
    goal="""Gerar um grafico de pizza visual com base nos dados de producao de cafe fornecidos
    """, 
    backstory=""" Você é especialista em visualização de
dados e transforma dados numéricos em gráficos claros e informativos .
    """,
    llm=llm,
    verbose=True, 
    allow_delegation=False,
    tools=[chart_tool]
)

coffee_research_task = Task(
    agent=research_agent,
    description="""
    Use o SerperDevTool para pesquisar a
    producao de cafe no Brasil por tipo de grao
    em 2024. Os tipos de cafe devem incluir: Acaia, Arara
    Bourbon, Catuai Amarelo, Catuai Vermelho, Caturra, Kona, Mundo Novo, Obata, Topazio 
    . As pesquisas na web devem ser feitas
    em fontes renomadas e retornar porcentagens para cada
    tipo de fonte
    """,
    expected_output="""
    Um dicionário com as porcentagens
    de producao de cafe em 2024 por tipo:
    {
        "Acaia": <valor>%, 
        "Arara": <valor>%,
        "Bourbon": <valor>%,
        "Catuai Amarelo": <valor>%,
        "Catuai Vermelho": <valor>%, 
        "Caturra": <valor>%, 
        "Kona": <valor>%, 
        "Mundo Novo": <valor>%, 
        "Obata": <valor>%, 
        "Topazio": <valor>%
    } 
    """,
    tools=[serper_tool]    
)

chart_creation_task = Task(
    description="""
    Utilize os dados de producao de cafe em 2024 para criar 
    um gráfico de pizza que ilustre a distribuição percentual de cada tipo
    de cafe : Acaia, Arara, Bourbon, Catuai Amarelo, Catuai Vermelho, 
    Caturra, Kona, Mundo Novo, Obata, Topazio 
    """,
    tools=[chart_tool],
    expected_output="Um grafico de pizza salvo como arquivo png que mostra a distribuicao do consumo de cafe por tipo",
    agent = chart_agent,
    context = [coffee_research_task]
)

coffee_crew = Crew(
    agents = [research_agent, chart_agent],
    tasks = [coffee_research_task, chart_creation_task],
    process = Process.sequential
)

result = coffee_crew.kickoff(inputs={})

print (f'Resultado: {result}')

