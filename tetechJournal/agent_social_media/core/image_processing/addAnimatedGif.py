from PIL import Image, ImageSequence

def adicionar_sticker_animado(
    base_path,
    gif_sticker_path,
    output_path,
    posicao=(0, 0)
):
    """
    Sobrepõe um GIF animado (sticker) em uma imagem base estática,
    gerando um novo GIF animado de saída.
    
    :param base_path: caminho da imagem de fundo (estática).
    :param gif_sticker_path: caminho do GIF do sticker animado.
    :param output_path: caminho do GIF final com a composição.
    :param posicao: tupla (x, y) onde o sticker será colocado em cada frame.
    """
    # 1. Carrega a imagem base em RGBA
    base_img = Image.open(base_path).convert("RGBA")
    w_base, h_base = base_img.size

    # 2. Abre o GIF animado do sticker
    sticker_gif = Image.open(gif_sticker_path)

    # Lista para armazenar frames resultantes
    frames_resultantes = []

    # 3. Itera pelos frames do sticker
    for frame in ImageSequence.Iterator(sticker_gif):
        # Converte frame para RGBA, garantindo canal alpha
        frame_rgba = frame.convert("RGBA")

        # Cria uma cópia da imagem base para compor
        frame_base_copia = base_img.copy()

        # 4. Faz a composição (alpha_composite) do frame do sticker sobre o fundo
        frame_base_copia.alpha_composite(frame_rgba, dest=posicao)

        # Adiciona ao array de frames resultantes
        frames_resultantes.append(frame_base_copia)

    # 5. Salva como GIF animado
    #    Usamos algumas infos do GIF original para manter a velocidade/duração
    #    Se não existir, definimos valores-padrão
    duration = sticker_gif.info.get('duration', 100)  # milissegundos por frame
    loop = sticker_gif.info.get('loop', 0)            # 0 -> repete infinito
    
    frames_resultantes[0].save(
        output_path,
        save_all=True,
        append_images=frames_resultantes[1:],
        duration=duration,
        loop=loop
    )

    # Fechamos o sticker para liberar recursos
    sticker_gif.close()

# Exemplo de uso:
# adicionar_sticker_animado(
#     "imagem_base.png",
#     "sticker_animado.gif",
#     "saida_animada.gif",
#     posicao=(50, 50)
# )

# Observações Importantes
# Tamanho da Base vs. Sticker

# Se o GIF do sticker for maior que a imagem base, podem ocorrer cortes ou “sobras”. Ajuste conforme necessário.
# Se precisar redimensionar o sticker (ou cada frame dele), faça isso dentro do loop, chamando frame_rgba = frame_rgba.resize((nova_largura, nova_altura), Image.LANCZOS) antes de compor.
# Transparência e Cores

# Se o sticker animado tiver fundo transparente, a camada RGBA será respeitada. Caso o fundo não seja transparente, você pode precisar criar uma máscara ou converter a cor de fundo em alpha.
# Caso o sticker não tenha canal alpha, frame.convert("RGBA") apenas cria um alpha 100% opaco.
# Disposal Method

# Alguns GIFs usam “disposal methods” para remover/restaurar parte do frame anterior ao desenhar o frame atual. Esse exemplo trata cada frame como se fosse completo (full-frame). Se o sticker animado tiver animações parciais, pode ser necessário um tratamento extra para compor corretamente. Entretanto, na maioria dos GIFs simples, esse método funciona bem.
# Sincronização de Frames

# Caso a imagem base também fosse animada (por exemplo, outro GIF de fundo), você teria que sincronizar frames do fundo e do sticker. A abordagem se torna mais complexa, pois cada GIF pode ter quantidades de frames e durações diferentes.
# Manter ou Personalizar Duração

# No exemplo, copiamos duration e loop do próprio sticker. Se quiser outro tempo de exibição, basta alterar duration. Se quiser parar em algum momento, ajuste loop (por exemplo, loop=1 para reproduzir só uma vez).
# Seguindo esse modelo, você consegue gerar um GIF final no qual o sticker animado aparece posicionado sobre a imagem base estática, quadro a quadro.