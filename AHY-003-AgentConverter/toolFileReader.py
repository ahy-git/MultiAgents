# file_reader_tool.py
from crewai.tools import BaseTool
from typing import Optional
import os

class FileReaderTool(BaseTool):
    name: str = "Leitor de Códigos Fonte"
    description: str = "Lê arquivos .py e exemplos de saída em uma pasta para análise posterior."
    folder: Optional[str] = "./input"
    
    def _read_py_files(self):
        py_files = {}
        for filename in os.listdir(self.folder):
            if filename.endswith(".py") and filename != "MyLLM.py":
                with open(os.path.join(self.folder, filename), "r", encoding="utf-8") as f:
                    py_files[filename] = f.read()
        return py_files

    def _read_output_examples(self):
        outputs = {}
        for filename in os.listdir(self.folder):
            if filename.startswith("example_output") and filename.endswith(".txt"):
                with open(os.path.join(self.folder, filename), "r", encoding="utf-8") as f:
                    outputs[filename] = f.read()
        return outputs

    def _run(self) -> str:
        py_files = self._read_py_files()
        outputs = self._read_output_examples()

        all_inputs = "\n\n".join([
            f"Arquivo: {name}\nConteúdo:\n{content}"
            for name, content in {**py_files, **outputs}.items()
        ])
        return all_inputs


# TESTE LOCAL INDEPENDENTE
if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base_dir, "../AWL-006-MusicGenerator"))
    print(f"Executando leitura de arquivos da pasta: {path}")
    tool = FileReaderTool(folder=path)
    resultado = tool._run()
    print(resultado)
