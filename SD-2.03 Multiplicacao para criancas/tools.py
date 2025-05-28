from crewai.tools import BaseTool

class MultiplicationTool(BaseTool):
    name: str="Ferramenta de mutliplicacao"
    description: str="Ferramenta util para quando precisa multiplicar dois numeros inteiros"
    
    def _run(self,primeiro_numero: int, segundo_numero: int) -> str:
        resultado = primeiro_numero * segundo_numero
        return f"""o produto de {primeiro_numero} x {segundo_numero} eh {resultado}
        """
