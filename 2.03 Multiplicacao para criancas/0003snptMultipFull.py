from crewai import Agent, Task, Crew, Process
from tools import MultiplicationTool
from dotenv import load_dotenv
from MyLLM import MyLLM

load_dotenv()

llm = MyLLM.geminiflash15

# instancia tool para uso posterior
multiplication_tool=MultiplicationTool()

generator_agent = Agent(
    role = "Gerador de Numeros",
    goal = "Voce cria dois numeros aleatorios para serem multiplicados",
    backstory="Voce eh especialista em gerar numeros aleatorios",
    allow_delegation=False,
    llm = llm,
    verbose = True
    )

writer_agent = Agent(
    role = "Escritor",
    goal ="Voce escreve licoes de  matematica para criancas",
    backstory=" Voce e' um especialista em readacao e adora ensinar criancas, mas nao sabe nada de matematica",
    allow_delegation=False,
    llm = llm,
    tools=[multiplication_tool],
    verbose = True
    )

generate_number_task = Task(
    description="Peca a LLM para gerar dois numero aleatorios entre 1 e 10",
    expected_output="dois numeros inteiros para serem multiplicados",
    agent=generator_agent
)

multiplication_task = Task(
    description="""
    Ensine a multiplicação para crianças.
    Multiplique os dois números fornecidos pelo agente
    Gerador de Números . Quando você for ensinar use
    maçãs ( emojis ) para explicar em um texto como
    funciona a multiplicação na linguagem
    para crianças
    """,
    expected_output=""" Uma explicação para crianças sobre
    multilicação. O primeiro número aleatório
    representa a quantidade de sacolas e o segundo
    número aleatório representa a quantidade de maçãs
    como mostra o exemplo delimitado por <exemplo>
    <exemplo>
    sacolas de maçãs:
    sacola 1: coloque aqui 3 emojs de maçãs
    sacola 2: coloque aqui 3 emojs de maçãs
    sacola 3: coloque aqui 3 emojs de maçãs
    Portanto : 3 x 4 = 12 maçãs
    </exemplo>
    """,
    tools = [multiplication_tool],
    agent=writer_agent
    
)

math_crew = Crew(
    agents=[generator_agent, writer_agent],
    tasks=[generate_number_task, multiplication_task],
    process=Process.sequential
)

result = math_crew.kickoff(inputs={})

print(f"Resultados final: {result} ")

