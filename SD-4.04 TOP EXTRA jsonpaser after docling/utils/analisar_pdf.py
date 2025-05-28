import fitz  # PyMuPDF

def analisar_pdf_para_pipeline(path_pdf):
    doc = fitz.open(path_pdf)
    num_paginas = len(doc)
    total_texto = 0
    total_imagens = 0
    paginas_com_pouco_texto = 0

    for page in doc:
        texto = page.get_text("text").strip()
        total_texto += len(texto)
        total_imagens += len(page.get_images(full=True))
        if len(texto) < 300:  # limiar de baixa densidade textual
            paginas_com_pouco_texto += 1

    densidade_textual = total_texto / max(num_paginas, 1)
    print(f"📄 {num_paginas} páginas | 📜 Texto total: {total_texto} | 🖼️ Imagens: {total_imagens}")

    usar_vlm = (
        total_imagens >= num_paginas // 2
        or densidade_textual < 500
        or paginas_com_pouco_texto > num_paginas * 0.4
    )

    return "vlm" if usar_vlm else "standard"