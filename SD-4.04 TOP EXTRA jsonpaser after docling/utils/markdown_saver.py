import os

def salvar_em_markdown(conteudo_md: str, caminho_saida: str = "resumo_final.md"):
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(conteudo_md)
    print(f"✅ Resumo final salvo com sucesso em: {caminho_saida}")


def salvar_resumos_em_arquivos(resumos: list, pasta_saida: str = "resumos"):
    """
    Salva cada item de `resumos` como um arquivo separado em formato Markdown.
    Os arquivos são nomeados como grupo_001.md, grupo_002.md, etc.
    """
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    caminhos = []
    for i, resumo in enumerate(resumos, start=1):
        caminho = os.path.join(pasta_saida, f"grupo_{i:03}.md")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(resumo.strip())
        caminhos.append(caminho)

    print(f"✅ {len(caminhos)} arquivos salvos em: {pasta_saida}/")
    return caminhos
