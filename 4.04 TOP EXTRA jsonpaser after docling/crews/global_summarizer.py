from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

load_dotenv()
llm='gemini/gemini-2.0-flash-lite'

def gerar_resumo_final(pasta="resumos"):
    arquivos = sorted(f for f in os.listdir(pasta) if f.endswith(".md"))
    textos = []

    for nome in arquivos:
        with open(os.path.join(pasta, nome), "r", encoding="utf-8") as f:
            texto = f.read()
            if len(texto.strip()) > 20:
                textos.append(f"### {nome}\n\n{texto.strip()}")

    texto_completo = "\n\n".join(textos)
    print(f"\n📄 Tamanho total do texto de entrada: {len(texto_completo)} caracteres")
    print(f"📚 Total de arquivos-parciais processados: {len(textos)}")
    print(f"🔎 Preview do início do input:\n{textos[0][:500]}")

    agente = Agent(
        role="Síntetizador Global",
        goal="Gerar um resumo final conciso com base em blocos reais de conteúdo.",
        backstory="Você é especialista em leitura crítica e síntese executiva de documentos técnicos.",
        tools=[],
        allow_delegation=False
    )

    task = Task(
        description=(
            "Você receberá o conteúdo real de diversos resumos parciais extraídos de um documento PDF.\n\n"
            "Gere um resumo final estruturado (em Markdown) com:\n"
            "- Objetivo do documento (inferido)\n"
            "- Principais tópicos abordados\n"
            "- Conclusões gerais\n"
            "- Recomendações finais\n\n"
            "⚠️ NÃO escreva templates ou placeholders. Extraia conteúdo real dos blocos apresentados.\n"
            "Use marcadores e subtítulos. Cite conteúdos-chave sempre que possível."
        ),
        expected_output="Resumo final técnico e real, baseado no conteúdo REAL dos resumos anteriores.",
        agent=agente,
        input=texto_completo
    )

    crew = Crew(agents=[agente], tasks=[task], process=Process.sequential)
    return crew.kickoff().raw