from docling.document_converter import DocumentConverter
from pathlib import Path
import json

source = "sample.pdf"  # Caminho local para o PDF
converter = DocumentConverter()
result = converter.convert(source)

# ✅ Corrigir caminho de saída com Path
output_path = Path(f"{source}.json")
with output_path.open("w", encoding="utf-8") as fp:
    json.dump(result.document.export_to_dict(), fp, ensure_ascii=False, indent=2)

# ✅ Exibir versão em Markdown no terminal
print(result.document.export_to_markdown())
