import os
import json
import time
import shutil
from random import randint
from pathlib import Path
from docling.document_converter import DocumentConverter

from crews.final_summarizer import gerar_resumo_final_robusto
from crews.section_summarizer import gerar_resumo_por_secao

from utils.docling_adapter import adaptar_json_docling
from utils.markdown_saver import salvar_em_markdown
from utils.detectar_ultimo_resumo import detectar_ultimo_index
from utils.analisar_pdf import analisar_pdf_para_pipeline



# Caminhos
pdf_input = "sample.pdf"
json_output = "sample.json"
resumo_final_path = "resumo_final.md"
resumo_dir = "resumos"



# Etapa 0: Executar Docling via DocumentConverter (não CLI)
if not os.path.exists(json_output):
    print("🚀 Executando Docling (DocumentConverter) para gerar JSON...")
    pipeline_recomendado = analisar_pdf_para_pipeline(pdf_input)
    converter = DocumentConverter(
                                # pipeline=pipeline_recomendado,
                                # ocr=True,
                                # enrich_picture_description=True,
                                # num_threads=8
                                  )
    result = converter.convert(pdf_input)

    # Salvar JSON
    with Path(json_output).open("w", encoding="utf-8") as fp:
        json.dump(result.document.export_to_dict(), fp, ensure_ascii=False, indent=2)

    print("✅ JSON gerado com sucesso!")

# Etapa 1: Adaptar JSON para seções
sections = adaptar_json_docling(json_output)
if not sections:
    print("❌ Nenhuma seção válida encontrada.")
    exit()

# Etapa 2: Processar e salvar cada resumo de seção
if not os.path.exists(resumo_dir):
    os.makedirs(resumo_dir)

# Detectar até onde já foi salvo
inicio = detectar_ultimo_index(resumo_dir)
print(f"🔁 Retomando a partir da seção {inicio + 1} (refazendo ela inclusive)")

for i, section in enumerate(sections, start=1):
    if i < inicio + 1:
        continue  # pula os já existentes

    print(f"📝 Processando seção {i}/{len(sections)}: {section.get('title', 'sem título')}")
    resumo = gerar_resumo_por_secao(section)
    caminho = os.path.join(resumo_dir, f"grupo_{i:03}.md")
    salvar_em_markdown(resumo, caminho_saida=caminho)
    print(f"✅ Salvo: {caminho}")
    
    time.sleep(randint(1,6))

# Etapa 3: Gerar o resumo final robusto
resumo_geral = gerar_resumo_final_robusto(resumo_dir)

# Etapa 4: Salvar o resumo final
salvar_em_markdown(resumo_geral, caminho_saida=resumo_final_path)
print(f"\n✅ Ciclo completo")


# Etapa 5: Limpar arquivos temporários
print("\n🧹 Limpando arquivos temporários...")

if os.path.exists(json_output):
    os.remove(json_output)
    print(f"🗑️ JSON removido: {json_output}")

if os.path.exists(resumo_dir):
    shutil.rmtree(resumo_dir)
    print(f"🗑️ Pasta de resumos removida: {resumo_dir}")
    
# ✏️ Renomear resumo_final.md → sample.md
pdf_stem = Path(pdf_input).stem
novo_nome = f"{pdf_stem}.md"
if os.path.exists(resumo_final_path):
    os.rename(resumo_final_path, novo_nome)
    print(f"📄 Arquivo final renomeado para: {novo_nome}")
    
print("✅ Limpeza finalizada.")
