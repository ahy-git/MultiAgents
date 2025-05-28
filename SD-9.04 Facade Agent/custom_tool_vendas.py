from pydantic import Field
from crewai.tools import BaseTool
import pandas as pd
import os
import traceback
import builtins

class QueryCSV(BaseTool):
    name: str = "Ferramenta de Execução de Código Python para Consulta em CSV"
    description: str = (
        "Executa um código Python seguro que consulta um CSV. "
        "O código deve ler o arquivo vendas_ficticias_brasil.csv, realizar uma análise com pandas "
        "e armazenar a resposta final na variável 'resultado', que será retornada pela ferramenta."
    )
    
    file_path: str = Field(default='vendas_ficticias_brasil.csv')

    def _run(self, codigo_python: str) -> str:
        contexto = {
            "__builtins__": {
                "sum": sum,
                "len": len,
                "print": print,
                "range": range,
                "min": min,
                "max": max,
                "round": round,
                "str": str,
                "int": int,
                "float": float,
                "__import__": builtins.__import__,  # <- Adicionado para permitir importações
            },
            "os": os,
            "pd": pd,
            "file_path": self.file_path
        }

        try:
            exec(codigo_python, contexto)
            if "resultado" not in contexto:
                return "Erro: o código não definiu a variável 'resultado'."
            return str(contexto["resultado"])
        except Exception as e:
            tb = traceback.format_exc()
            return f"Erro ao executar o código Python:\n{str(e)}\n\nDetalhes:\n{tb}"
