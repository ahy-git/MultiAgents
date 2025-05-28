from crewai_tools import tool

@tool("Multiplication Tool")
def multiplicationTool(primeiro_numero: int,
                       segundo_numero: int) -> str:
    
    resultado = primeiro_numero * segundo_numero
    
    return f'A multiplicacao de {primeiro_numero} x {segundo_numero} eh igual a {resultado}'


