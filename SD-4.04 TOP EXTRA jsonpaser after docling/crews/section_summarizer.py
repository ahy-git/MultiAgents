from crewai import Agent, Task, Crew, Process
from .tools.section_text_tool import SectionTextTool
from dotenv import load_dotenv

load_dotenv()
llm='gemini/gemini-2.0-flash-lite'

def gerar_resumo_por_secao(section):
    tool = SectionTextTool(section_text=section["text"])
    
    agente = Agent(
        role="Resumidor de Seção",
        goal="Resumir seções longas de documentos PDF em linguagem objetiva",
        backstory="Você é um especialista em síntese de documentos técnicos.",
        tools=[tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

    task = Task(
        description=(
            f"Resuma de forma clara e estruturada a seguinte seção do documento: '{section.get('title', 'Seção sem título')}'.\n\n"
            "Seu resumo deve conter:\n"
            "- Objetivo da seção\n"
            "- Tópicos principais\n"
            "- Informações relevantes\n"
            "- Uma citação direta representativa\n\n"
            "Evite repetir o texto literalmente. Seja técnico e objetivo."
        ),
        expected_output="Um resumo objetivo da seção.",
        agent=agente
    )

    crew = Crew(agents=[agente], tasks=[task], process=Process.sequential)
    return crew.kickoff().raw
