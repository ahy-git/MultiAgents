import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from .tools.text_block_tool import TextBlockTool

load_dotenv()
llm='gemini/gemini-2.0-flash-lite'

# ✅ FILTRA resumos inválidos, curtos ou com placeholders
def carregar_textos_validos(pasta):
    arquivos = sorted(f for f in os.listdir(pasta) if f.endswith(".md"))
    textos_validos = []
    for nome in arquivos:
        with open(os.path.join(pasta, nome), "r", encoding="utf-8") as f:
            texto = f.read().strip()
            if len(texto) > 100 and "preencher com" not in texto.lower() and "insert the" not in texto.lower():
                textos_validos.append(f"### {nome}\n\n{texto}")
    return textos_validos

# ✅ RESUME RECURSIVAMENTE até chegar a <30k caracteres
def resumir_blocos_recursivamente(textos, profundidade=1):
    texto_completo = "\n\n".join(textos)
    if len(texto_completo) < 30000 or len(textos) == 1:
        return texto_completo

    blocos = 3
    blocos_de_texto = []
    blocos_tam = len(textos) // blocos
    for i in range(blocos):
        subset = textos[i * blocos_tam : (i + 1) * blocos_tam]
        blocos_de_texto.append("\n\n".join(subset))

    resumos_parciais = []
    for i, bloco in enumerate(blocos_de_texto, start=1):
        print(f"📦 Resumindo bloco {i}/{blocos} (nível {profundidade})")

        tool = TextBlockTool(bloco=bloco)

        agente = Agent(
            role=f"Resumidor Nível {profundidade}",
            goal="Gerar um resumo parcial conciso com base em textos agrupados.",
            backstory="Você resume grandes blocos temáticos de forma clara e objetiva.",
            tools=[tool],
            llm=llm,
            verbose=True,
            allow_delegation=False
        )

        task = Task(
            description=(
                f"Você recebeu um grupo de resumos (Bloco {i}) relacionados ao mesmo documento.\n\n"
                "Use a ferramenta 'Bloco de Texto' para acessar o conteúdo.\n"
                "Gere um resumo parcial, com foco em:\n"
                "- Objetivo geral\n"
                "- Principais temas\n"
                "- Conclusões\n"
                "- Recomendações\n"
            ),
            expected_output="Resumo parcial em markdown com subtítulos.",
            agent=agente
        )

        crew = Crew(agents=[agente], tasks=[task], process=Process.sequential)
        resumos_parciais.append(crew.kickoff().raw)

    return resumir_blocos_recursivamente(resumos_parciais, profundidade=profundidade + 1)

# ✅ INTERFACE PRINCIPAL
def gerar_resumo_final_robusto(pasta="resumos"):
    textos_validos = carregar_textos_validos(pasta)
    if not textos_validos:
        return "❌ Nenhum conteúdo válido encontrado nos arquivos .md"
    return resumir_blocos_recursivamente(textos_validos)
