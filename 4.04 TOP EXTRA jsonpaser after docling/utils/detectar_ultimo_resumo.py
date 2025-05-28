import os

def detectar_ultimo_index(resumo_dir):
    arquivos = sorted([
        f for f in os.listdir(resumo_dir) if f.startswith("grupo_") and f.endswith(".md")
    ])
    if not arquivos:
        return 0
    ultimo = arquivos[-1]
    numero = int(ultimo.replace("grupo_", "").replace(".md", ""))
    return numero - 1  # recomeça do último já existente