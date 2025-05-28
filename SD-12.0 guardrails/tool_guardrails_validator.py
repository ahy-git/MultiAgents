from guardrails import Guard
from pydantic import BaseModel, PrivateAttr
from typing import Dict
from crewai.tools import BaseTool

class ProfileSchema(BaseModel):
    name: str
    age: int
    profession: str

class GuardrailsValidatorTool(BaseTool):
    name: str = "Guardrails Output Validator" 
    description: str = "Valida a saída JSON de um agente baseada em um schema"

    _guard: Guard = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._guard = Guard.from_pydantic(ProfileSchema)

    def _run(self, output: str) -> Dict:
        result = self._guard.parse(output)
        failed = not result.validation_passed
        summaries = result.validation_summaries or ["O output não está em conformidade com o schema."]
        raw_llm_output = result.raw_llm_output
        reask = result.reask
        
        return {
            "valid": not failed,
            "error": "\n".join([
                                *summaries,
                                "<output>",
                                str(raw_llm_output),
                                "</output>",
                                "<analisis>",
                                str(reask),
                                "</analisis>"
                            ]),
            "output": result.validated_output if not failed else None,
            "raw_output": output if failed else None
        }
