from PIL import Image
# Este exemplo aplica uma transformação afim para “inclinar” a imagem. A transformação afim é definida por uma matriz 3×3 (mas a PIL utiliza 6 coeficientes), onde você pode criar efeitos de distorção, rodar, transladar, etc.
def affine_transform_demo(img_path, output_path):
    # Abre a imagem original
    img = Image.open(img_path)

    # Dimensões
    w, h = img.size

    # Coeficientes para transformação afim
    # (a, b, c, d, e, f)
    # Equação: x' = a*x + b*y + c
    #          y' = d*x + e*y + f
    # Exemplo: "inclinar" a parte superior para a direita
    a = 1
    b = 0.3
    c = 0
    d = 0
    e = 1
    f = 0

    # Aplica a transformação afim
    img_transformed = img.transform(
        (w, h),               # tamanho de saída (mesmo da original)
        Image.AFFINE,         # tipo de transformação
        (a, b, c, d, e, f),   # parâmetros
        resample=Image.BICUBIC
    )

    img_transformed.save(output_path)

# Exemplo de uso
# affine_transform_demo("imagem_original.jpg", "imagem_inclinada.jpg")

###########################
from PIL import Image
# A transformação em perspectiva (Image.PERSPECTIVE) permite criar efeitos de “desaparecimento” de um canto a outro, simulando profundidade.

def perspective_transform_demo(img_path, output_path):
    img = Image.open(img_path)
    w, h = img.size

    # Mapeamento de 4 pontos de um quadrilátero de origem
    # para outro quadrilátero de destino
    # data é tupla de 8 floats, representando a projeção
    # Equação envolve resolução de sistemas, mas pode usar libs de geometria
    # Exemplo simples: puxar o topo para dentro, gerando "efeito trapezoidal"
    data = (
        0.7, 0.2,   # canto superior esquerdo
        0.3, 0,     # canto superior direito
        0,   1.2,   # canto inferior esquerdo
        1,   1      # canto inferior direito
    )

    img_persp = img.transform(
        (w, h),
        Image.PERSPECTIVE,
        data,
        resample=Image.BICUBIC
    )

    img_persp.save(output_path)

# Exemplo de uso
# perspective_transform_demo("imagem_original.jpg", "imagem_perspectiva.jpg")

###################
# Usando ImageFilter.Kernel, você pode aplicar convoluções 2D personalizadas sobre a imagem (por exemplo, filtros de detecção de borda, sharpen, emboss, etc.).

from PIL import Image, ImageFilter

def custom_kernel_demo(img_path, output_path):
    img = Image.open(img_path).convert("RGB")

    # Exemplo: filtro de nitidez básico (sharpen)
    # Dimensão do kernel: 3x3
    # A soma dos pesos deve ser > 0 para não resultar em imagem totalmente preta ou branca
    kernel = [
        0, -1,  0,
        -1, 5, -1,
        0, -1,  0
    ]

    custom_filter = ImageFilter.Kernel(
        size=(3, 3),    # Tamanho do kernel
        kernel=kernel,  # Lista de pesos
        scale=None,     # Normalização automática
        offset=0        # Deslocamento
    )

    img_filtered = img.filter(custom_filter)
    img_filtered.save(output_path)

# Exemplo de uso
# custom_kernel_demo("entrada.jpg", "sharpened.jpg")

###########################################
# Às vezes, você quer usar NumPy para uma manipulação mais sofisticada (como aplicar algoritmos de visão computacional personalizados) e então retornar para a PIL para salvar ou mostrar a imagem.



import numpy as np
from PIL import Image

def numpy_pipeline_demo(img_path, output_path):
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img)  # Converte PIL -> NumPy (altura x largura x canais)

    # Exemplo simples: inverter só o canal Red
    # arr[..., 0] representa o canal R (vermelho)
    arr[..., 0] = 255 - arr[..., 0]

    # Cria uma nova imagem a partir do array modificado
    new_img = Image.fromarray(arr)
    new_img.save(output_path)

# Exemplo
# numpy_pipeline_demo("foto_original.jpg", "foto_invert_red.jpg")

#######################
# Usar máscaras permite editar apenas certas partes da imagem. Neste exemplo, criamos uma máscara circular e aplicamos um efeito de desfoque apenas dentro desse círculo.
from PIL import Image, ImageDraw, ImageFilter

def blur_with_mask_demo(img_path, output_path):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size

    # Passo 1: criar imagem desfocada
    blurred = img.filter(ImageFilter.GaussianBlur(radius=10))

    # Passo 2: criar uma máscara (tons de cinza) para definir a área de aplicação
    # Aqui, vamos desenhar um círculo central
    mask = Image.new("L", (w, h), 0)  # “L” = 8 bits (tons de cinza), 0=preto
    draw = ImageDraw.Draw(mask)
    cx, cy = w // 2, h // 2
    r = min(w, h) // 4  # Raio do círculo
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=255)  # 255=branco

    # Passo 3: Fazer o composite combinando área desfocada na máscara branca com imagem original
    result = Image.composite(blurred, img, mask)
    result.save(output_path)

# Exemplo
# blur_with_mask_demo("entrada.jpg", "saida_com_mask.jpg")

#####################
#  Podemos utilizar estatísticas da imagem para decidir como aplicar ajustes de cor e contraste. Aqui, medimos o brilho médio e, se estiver abaixo de um limiar, aumentamos o brilho; caso contrário, aplicamos maior contraste.
from PIL import Image, ImageEnhance, ImageStat

def smart_adjust_demo(img_path, output_path):
    img = Image.open(img_path).convert("RGB")

    # Estatísticas
    stat = ImageStat.Stat(img)
    mean_brightness = sum(stat.mean) / 3  # Média do R, G, B

    if mean_brightness < 100:
        # Aumenta brilho
        enhancer = ImageEnhance.Brightness(img)
        img_enh = enhancer.enhance(1.5)
    else:
        # Aumenta contraste
        enhancer = ImageEnhance.Contrast(img)
        img_enh = enhancer.enhance(1.5)

    img_enh.save(output_path)

# Exemplo
# smart_adjust_demo("subexposta.jpg", "saida_ajustada.jpg")

###########################################
# Podemos utilizar estatísticas da imagem para decidir como aplicar ajustes de cor e contraste. Aqui, medimos o brilho médio e, se estiver abaixo de um limiar, aumentamos o brilho; caso contrário, aplicamos maior contraste.

from PIL import Image, ImageEnhance, ImageStat

def smart_adjust_demo(img_path, output_path):
    img = Image.open(img_path).convert("RGB")

    # Estatísticas
    stat = ImageStat.Stat(img)
    mean_brightness = sum(stat.mean) / 3  # Média do R, G, B

    if mean_brightness < 100:
        # Aumenta brilho
        enhancer = ImageEnhance.Brightness(img)
        img_enh = enhancer.enhance(1.5)
    else:
        # Aumenta contraste
        enhancer = ImageEnhance.Contrast(img)
        img_enh = enhancer.enhance(1.5)

    img_enh.save(output_path)

# Exemplo
# smart_adjust_demo("subexposta.jpg", "saida_ajustada.jpg")

############################################
# Você pode iterar sobre cada frame de um GIF animado, aplicar transformações e salvar novamente como um GIF. No exemplo, cada quadro será convertido em tons de cinza.

from PIL import Image, ImageSequence

def gif_grayscale_demo(gif_path, output_path):
    img_gif = Image.open(gif_path)

    # Lista para armazenar frames processados
    frames_modificados = []

    for frame in ImageSequence.Iterator(img_gif):
        # Converte para 'RGB' ou 'RGBA' antes de passar para grayscale
        frame_rgb = frame.convert("RGB")
        gray_frame = frame_rgb.convert("L")

        # Converte de volta para 'P' (paleta) se quiser manter modo GIF otimizado
        frame_p = gray_frame.convert("P", palette=Image.ADAPTIVE)
        frames_modificados.append(frame_p)

    # Salva como GIF animado
    frames_modificados[0].save(
        output_path,
        save_all=True,
        append_images=frames_modificados[1:],
        loop=0,
        duration=img_gif.info.get('duration', 100)  # mantém duração original
    )

# Exemplo
# gif_grayscale_demo("animacao.gif", "animacao_gray.gif")

##############################
# Este script faz várias etapas em sequência:

# Redimensiona para um tamanho menor (thumbnail).
# Aplica correção de cor (ajuste de saturação).
# Realça detalhe com um kernel de nitidez customizado.
# Sobrepõe uma marca d’água (watermark) no canto inferior direito com semi-transparência.

from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

def advanced_pipeline_demo(img_path, watermark_path, output_path):
    # 1. Abre imagem e redimensiona
    img = Image.open(img_path).convert("RGB")
    img.thumbnail((1024, 1024))

    # 2. Aumenta saturação
    color_enhancer = ImageEnhance.Color(img)
    img_saturated = color_enhancer.enhance(1.2)  # fator de saturação

    # 3. Aplica filtro de nitidez customizado
    sharpen_kernel = [ 0, -1, 0,
                      -1,  5, -1,
                       0, -1, 0 ]
    kernel_filter = ImageFilter.Kernel((3,3), sharpen_kernel)
    img_sharpened = img_saturated.filter(kernel_filter)

    # 4. Cria objeto RGBA para compor marca d'água
    base_rgba = img_sharpened.convert("RGBA")

    # Carrega e redimensiona watermark
    watermark = Image.open(watermark_path).convert("RGBA")
    w_wm, h_wm = watermark.size
    scale_factor = 0.3
    watermark = watermark.resize((int(w_wm * scale_factor), int(h_wm * scale_factor)))

    # Ajusta a opacidade da marca d'água
    alpha = 100  # valor entre 0-255
    wm_data = watermark.getdata()
    new_data = []
    for item in wm_data:
        # item é (R, G, B, A)
        new_data.append((item[0], item[1], item[2], alpha))
    watermark.putdata(new_data)

    # Determina posição no canto inferior direito
    W, H = base_rgba.size
    w_wm, h_wm = watermark.size
    pos = (W - w_wm - 20, H - h_wm - 20)

    # 5. Sobrepõe (composite) a marca d’água
    base_rgba.alpha_composite(watermark, dest=pos)

    # Converte de volta para RGB e salva
    final_img = base_rgba.convert("RGB")
    final_img.save(output_path)

# Exemplo
# advanced_pipeline_demo("entrada.jpg", "watermark.png", "saida_final.jpg")
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

def advanced_pipeline_demo(img_path, watermark_path, output_path):
    # 1. Abre imagem e redimensiona
    img = Image.open(img_path).convert("RGB")
    img.thumbnail((1024, 1024))

    # 2. Aumenta saturação
    color_enhancer = ImageEnhance.Color(img)
    img_saturated = color_enhancer.enhance(1.2)  # fator de saturação

    # 3. Aplica filtro de nitidez customizado
    sharpen_kernel = [ 0, -1, 0,
                      -1,  5, -1,
                       0, -1, 0 ]
    kernel_filter = ImageFilter.Kernel((3,3), sharpen_kernel)
    img_sharpened = img_saturated.filter(kernel_filter)

    # 4. Cria objeto RGBA para compor marca d'água
    base_rgba = img_sharpened.convert("RGBA")

    # Carrega e redimensiona watermark
    watermark = Image.open(watermark_path).convert("RGBA")
    w_wm, h_wm = watermark.size
    scale_factor = 0.3
    watermark = watermark.resize((int(w_wm * scale_factor), int(h_wm * scale_factor)))

    # Ajusta a opacidade da marca d'água
    alpha = 100  # valor entre 0-255
    wm_data = watermark.getdata()
    new_data = []
    for item in wm_data:
        # item é (R, G, B, A)
        new_data.append((item[0], item[1], item[2], alpha))
    watermark.putdata(new_data)

    # Determina posição no canto inferior direito
    W, H = base_rgba.size
    w_wm, h_wm = watermark.size
    pos = (W - w_wm - 20, H - h_wm - 20)

    # 5. Sobrepõe (composite) a marca d’água
    base_rgba.alpha_composite(watermark, dest=pos)

    # Converte de volta para RGB e salva
    final_img = base_rgba.convert("RGB")
    final_img.save(output_path)

# Exemplo
# advanced_pipeline_demo("entrada.jpg", "watermark.png", "saida_final.jpg")
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

def advanced_pipeline_demo(img_path, watermark_path, output_path):
    # 1. Abre imagem e redimensiona
    img = Image.open(img_path).convert("RGB")
    img.thumbnail((1024, 1024))

    # 2. Aumenta saturação
    color_enhancer = ImageEnhance.Color(img)
    img_saturated = color_enhancer.enhance(1.2)  # fator de saturação

    # 3. Aplica filtro de nitidez customizado
    sharpen_kernel = [ 0, -1, 0,
                      -1,  5, -1,
                       0, -1, 0 ]
    kernel_filter = ImageFilter.Kernel((3,3), sharpen_kernel)
    img_sharpened = img_saturated.filter(kernel_filter)

    # 4. Cria objeto RGBA para compor marca d'água
    base_rgba = img_sharpened.convert("RGBA")

    # Carrega e redimensiona watermark
    watermark = Image.open(watermark_path).convert("RGBA")
    w_wm, h_wm = watermark.size
    scale_factor = 0.3
    watermark = watermark.resize((int(w_wm * scale_factor), int(h_wm * scale_factor)))

    # Ajusta a opacidade da marca d'água
    alpha = 100  # valor entre 0-255
    wm_data = watermark.getdata()
    new_data = []
    for item in wm_data:
        # item é (R, G, B, A)
        new_data.append((item[0], item[1], item[2], alpha))
    watermark.putdata(new_data)

    # Determina posição no canto inferior direito
    W, H = base_rgba.size
    w_wm, h_wm = watermark.size
    pos = (W - w_wm - 20, H - h_wm - 20)

    # 5. Sobrepõe (composite) a marca d’água
    base_rgba.alpha_composite(watermark, dest=pos)

    # Converte de volta para RGB e salva
    final_img = base_rgba.convert("RGB")
    final_img.save(output_path)

# Exemplo
# advanced_pipeline_demo("entrada.jpg", "watermark.png", "saida_final.jpg")
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

def advanced_pipeline_demo(img_path, watermark_path, output_path):
    # 1. Abre imagem e redimensiona
    img = Image.open(img_path).convert("RGB")
    img.thumbnail((1024, 1024))

    # 2. Aumenta saturação
    color_enhancer = ImageEnhance.Color(img)
    img_saturated = color_enhancer.enhance(1.2)  # fator de saturação

    # 3. Aplica filtro de nitidez customizado
    sharpen_kernel = [ 0, -1, 0,
                      -1,  5, -1,
                       0, -1, 0 ]
    kernel_filter = ImageFilter.Kernel((3,3), sharpen_kernel)
    img_sharpened = img_saturated.filter(kernel_filter)

    # 4. Cria objeto RGBA para compor marca d'água
    base_rgba = img_sharpened.convert("RGBA")

    # Carrega e redimensiona watermark
    watermark = Image.open(watermark_path).convert("RGBA")
    w_wm, h_wm = watermark.size
    scale_factor = 0.3
    watermark = watermark.resize((int(w_wm * scale_factor), int(h_wm * scale_factor)))

    # Ajusta a opacidade da marca d'água
    alpha = 100  # valor entre 0-255
    wm_data = watermark.getdata()
    new_data = []
    for item in wm_data:
        # item é (R, G, B, A)
        new_data.append((item[0], item[1], item[2], alpha))
    watermark.putdata(new_data)

    # Determina posição no canto inferior direito
    W, H = base_rgba.size
    w_wm, h_wm = watermark.size
    pos = (W - w_wm - 20, H - h_wm - 20)

    # 5. Sobrepõe (composite) a marca d’água
    base_rgba.alpha_composite(watermark, dest=pos)

    # Converte de volta para RGB e salva
    final_img = base_rgba.convert("RGB")
    final_img.save(output_path)

# Exemplo
# advanced_pipeline_demo("entrada.jpg", "watermark.png", "saida_final.jpg")
###############################

# Visao do diretor criativo gpt o1 
# Sugestões em alto nível (visão de “diretor criativo”):

# Correção de Tom e Cor
# A imagem parece um pouco acinzentada. Eu ajustaria o contraste e a saturação para ressaltar as cores dos personagens e dar uma vivacidade maior.
# Se o cenário tem uma tonalidade pastel, podemos enfatizar essa suavidade com um leve ajuste de brilho ou equalização para reforçar a atmosfera de “sonho” ou fantasia.

# Ajustes Básicos
# Brilho e Contraste: Subiria um pouco o brilho para deixar a imagem menos “escura” e adicionaria contraste para destacar as áreas claras versus as áreas escuras.
# Saturação ou “Coloração”: Se a imagem estiver meio opaca, aumentaria levemente a saturação para as cores ficarem mais vivas.
# Temperatura / Calor: Se quiser uma imagem mais “quente” (tons amarelados) ou “fria” (tons azulados). Depende do clima desejado.

# Ferramentas de Texto e Stickers
# Adicionaria um texto curto ou um adesivo (sticker) que combine com o tema. Por exemplo, algo que indique o tom (fantasia, lúdico) ou uma pequena legenda que explique a cena.
# Poderia inserir, por exemplo, uma cor de caixa de texto que combine com os personagens. Se houver algum texto automático (como parâmetros de geração), eu esconderia com um sticker ou usando a própria ferramenta de pincel para desenhar por cima.
# Desenho à Mão Livre (Brush/Pen)

# Caso queira dar um toque pessoal, abriria a ferramenta de desenho e faria linhas suaves ou setas indicando algo bacana na imagem. Também posso usar uma “caneta” de cor complementar para adicionar bordas ou contornos discretos.

# Foco Visual e Composição
# Verificar se há algum espaço vazio muito grande que não traga valor à composição. Talvez um corte (crop) para destacar os personagens principais, mantendo apenas o essencial.
# Se quisermos preservar a composição e dar uma sensação de profundidade, poderíamos aplicar um desfoque Gaussian no plano de fundo, realçando ainda mais os elementos em primeiro plano.

# Elementos Gráficos / Texto
# Dependendo da mensagem que você quer passar no stories, inserir uma pequena legenda ou um título estilizado (usando ImageDraw e ImageFont) pode dar um ar profissional.
# Você pode desenhar formas suaves ou pequenos ícones na borda para criar uma moldura personalizada.

# Estilo / Filtro Personalizado
# Podemos criar ou aplicar um filtro de cor (por exemplo, puxar levemente para o azul ou rosa) para homogeneizar os tons e dar assinatura visual.
# Usar convolução com um kernel estilizado (leve sharpen + realce de contorno) para trazer definição aos contornos dos personagens.

# Remoção ou Ocultação de Texto Indesejado
# Se existir alguma tarja ou algum texto automático no canto (como parâmetros de geração), podemos recortar, pintar ou sobrepor um retângulo de cor sólida e inserir uma etiqueta ou sticker no lugar.

# Adição de Camadas de Overlay
# Se a ideia for algo lúdico, pode-se incluir elementos de desenho (borrões de cor, pinceladas) como se fosse uma pintura digital por cima, simulando aquarela ou pastel.
# Uma textura de grão (“grain” ou “noise”) suave pode dar um toque mais cinematográfico.