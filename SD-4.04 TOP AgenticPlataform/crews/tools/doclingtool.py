# tools/doclingtool.py

from crewai.tools import BaseTool
from docling_parse import pdf_parser
from pydantic import Field

class PdfReaderTool(BaseTool):
    name: str = "Docling PDF Reader"
    description: str = "Lê um PDF com a biblioteca Docling e retorna o texto unificado extraído."
    pdf_path: str = Field(..., description="Caminho do arquivo PDF a ser processado")
    
    def __init__(self, pdf_path: str):
        super().__init__()
        self.pdf_path = pdf_path

    def _run(self) -> str:
        try:
            # Usa o parser do docling
            doc = pdf_parser(self.pdf_path)

            # Extrai o texto das seções (ajustável conforme estrutura do docling)
            texto = "\n".join(section.text for section in doc.sections if section.text)
            return texto or "Nenhum texto encontrado no PDF."
        except Exception as e:
            return f"Erro ao processar PDF com docling: {str(e)}"
