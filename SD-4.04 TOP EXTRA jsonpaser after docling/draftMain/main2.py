import os
import subprocess
from crews.section_summarizer import gerar_resumo_por_secao
from utils.docling_adapter import adaptar_json_docling
from utils.markdown_saver import salvar_em_markdown
from crews.final_summarizer import gerar_resumo_final_robusto

# Caminhos
pdf_input = "sample.pdf"
json_output = "sample.json"
resumo_final_path = "resumo_final.md"
resumo_dir = "resumos"

# Etapa 0: Executar Docling CLI
if not os.path.exists(json_output):
    print("🚀 Executando Docling para gerar o JSON...")
    comando = [
        "docling",
        "--from", "pdf",
        "--to", "json",
        "--enrich-picture-description",
        "-vv",
        "--num-threads","8",
        pdf_input
    ]
    resultado = subprocess.run(comando, capture_output=True, text=True)

    if resultado.returncode != 0:
        print("❌ Erro ao rodar o docling:")
        print(resultado.stderr)
        exit()
    print("✅ JSON gerado com sucesso!")

# Etapa 1: Adaptar JSON para seções
sections = adaptar_json_docling(json_output)
if not sections:
    print("❌ Nenhuma seção válida encontrada.")
    exit()

# Etapa 2: Processar e salvar cada resumo de seção
if not os.path.exists(resumo_dir):
    os.makedirs(resumo_dir)

for i, section in enumerate(sections, start=1):
    print(f"📝 Processando seção {i}/{len(sections)}: {section.get('title', 'sem título')}")
    resumo = gerar_resumo_por_secao(section)
    caminho = os.path.join(resumo_dir, f"grupo_{i:03}.md")
    salvar_em_markdown(resumo, caminho_saida=caminho)

# Etapa 3: Gerar o resumo final robusto
resumo_geral = gerar_resumo_final_robusto(resumo_dir)

# Etapa 4: Salvar o resumo final
salvar_em_markdown(resumo_geral, caminho_saida=resumo_final_path)
print(f"\n✅ Resumo final salvo em: {resumo_final_path}")
