from crewai.tools import BaseTool
from pydantic import Field

class TextBlockTool(BaseTool):
    name: str = "Bloco de Texto"
    description: str = "Fornece o conteúdo de um bloco de texto para ser analisado."

    bloco: str = Field(..., description="Texto consolidado de um grupo de resumos.")

    def _run(self) -> str:
        return self.bloco
