from PIL import Image

def adicionar_sticker(
    imagem_base_path,
    sticker_path,
    saida_path,
    posicao=(0, 0),
    nova_dimensao=None,  # Ex.: (largura, altura)
    angulo=0             # Ângulo em graus para rotação
):
    """
    Adiciona um sticker na imagem base, com opções de redimensionar e rotacionar.
    :param imagem_base_path: Caminho da imagem base.
    :param sticker_path: Caminho do sticker (PNG com transparência).
    :param saida_path: Caminho para salvar a imagem resultante.
    :param posicao: Tupla (x, y) indicando a posição superior esquerda onde o sticker será colado.
    :param nova_dimensao: Tupla (nova_largura, nova_altura) para redimensionar o sticker. Se None, mantém o tamanho original.
    :param angulo: Ângulo de rotação em graus (0 = sem rotação). Rotaciona em sentido anti-horário.
    """
    
    # 1. Abre a imagem base em RGBA
    base_img = Image.open(imagem_base_path).convert("RGBA")
    
    # 2. Abre o sticker também em RGBA
    sticker = Image.open(sticker_path).convert("RGBA")
    
    # 3. (Opcional) Redimensionar o sticker
    if nova_dimensao is not None:
        sticker = sticker.resize(nova_dimensao, Image.Resampling.LANCZOS)
        # Ou, em versões mais antigas do Pillow, use Image.ANTIALIAS
    
    # 4. (Opcional) Rotacionar o sticker
    if angulo != 0:
        # expand=True faz o sticker rotacionado não “cortar” as bordas
        sticker = sticker.rotate(angulo, expand=True)
    
    # 5. Cola o sticker na base, usando o próprio sticker como máscara (para preservar transparência)
    base_img.paste(sticker, posicao, sticker)
    
    # 6. Salva a imagem resultante
    base_img.save(saida_path)

# Exemplo de uso:
# adicionar_sticker(
#     "imagem_base.jpg",
#     "sticker.png",
#     "resultado.png",
#     posicao=(50, 50),
#     nova_dimensao=(100, 100),  # Redimensiona para 100x100 pixels
#     angulo=45                  # Rotaciona 45 graus
# )
