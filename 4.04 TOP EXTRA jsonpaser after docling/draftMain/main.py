from crews.section_summarizer import gerar_resumo_por_secao
from utils.docling_adapter import adaptar_json_docling
from utils.markdown_saver import salvar_em_markdown
from crews.final_summarizer import gerar_resumo_final_robusto

# Etapa 1: Adaptar JSON para formato unificado de seções
sections = adaptar_json_docling("parsed_output.json")
if not sections:
    print("❌ Nenhuma seção válida encontrada.")
    exit()

# Etapa 2: Processar cada seção --- Nao seria melhor ir salvando aqui?
resumos = []
for i, section in enumerate(sections, start=1):
    print(f"Processando seção: {section.get('title', 'sem título')}")
    resumo = gerar_resumo_por_secao(section)
    caminho = f"resumos/grupo_{i:03}.md"
    salvar_em_markdown(resumo, caminho_saida=caminho)


resumo_geral = gerar_resumo_final_robusto("resumos")

salvar_em_markdown(resumo_geral, caminho_saida="resumo_final.md")



