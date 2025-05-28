from crewai.tools import BaseTool
from pydantic import Field

class SectionTextTool(BaseTool):
    name: str = "Texto da Seção"
    description: str = "Fornece o texto completo de uma seção de um documento estruturado."

    section_text: str = Field(..., description="Texto da seção a ser analisada")

    def _run(self) -> str:
        return self.section_text
