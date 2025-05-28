import json
import math

def adaptar_json_docling(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sections = []

    # Caso clássico: já vem estruturado
    if "sections" in data and isinstance(data["sections"], list):
        print("🔍 Estrutura detectada: sections[]")
        sections = data["sections"]

    # Caso estruturado por páginas (mais comum com parser moderno)
    elif "pages" in data and isinstance(data["pages"], list):
        print("🔍 Estrutura detectada: pages[]")

        for i, page in enumerate(data["pages"]):
            texto = (
                page.get("text") or
                page.get("content") or
                "\n".join(page.get("lines", [])) or
                ""
            )
            if texto and len(texto.strip()) > 20:
                sections.append({
                    "title": f"Página {i+1}",
                    "text": texto.strip()
                })

    # Caso contenha bloco de textos puros
    elif "texts" in data and isinstance(data["texts"], list):
        print("🔍 Estrutura detectada: texts[]")

        for i, bloco in enumerate(data["texts"]):
            texto = bloco.get("text") or bloco.get("content") or ""
            if texto and len(texto.strip()) > 20:
                sections.append({
                    "title": f"Trecho {i+1}",
                    "text": texto.strip()
                })

    # Fallback vazio
    else:
        print("⚠️ Nenhuma estrutura conhecida detectada.")
        return []



    print(f"✅ {len(sections)} seções extraídas inicialmente.")

    # 🧠 Calcular o tamanho ideal para garantir no máximo 100 blocos
    tamanho_grupo = math.ceil(len(sections) / 100)
    print(f"🔧 Agrupando a cada {tamanho_grupo} seção(ões) para limitar a 100 blocos.")

    agrupadas = []
    for i in range(0, len(sections), tamanho_grupo):
        grupo = sections[i:i + tamanho_grupo]
        titulo_grupo = " + ".join(sec.get("title", f"Bloco {i + j + 1}") for j, sec in enumerate(grupo))
        texto_grupo = "\n\n".join(sec.get("text", "") for sec in grupo)

        agrupadas.append({
            "title": f"Grupo {i // tamanho_grupo + 1}: {titulo_grupo}",
            "text": texto_grupo
        })

    print(f"✅ {len(agrupadas)} seções agrupadas.")
    return agrupadas