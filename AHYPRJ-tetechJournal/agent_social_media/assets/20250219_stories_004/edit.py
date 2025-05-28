from PIL import Image, ImageEnhance, ImageDraw, ImageFont

def editar_imagem_dog(input_path, output_path):
    """
    Faz edições na imagem do dog (como ajustes de cor, nitidez e adiciona texto).
    Gera a imagem final em output_path.
    """

    # 1) ABRIR A IMAGEM
    img = Image.open(input_path).convert("RGB")

    # 2) AJUSTAR BRILHO, CONTRASTE, SATURAÇÃO E NITIDEZ
    #    (valores de 1.0 significam "sem alteração"; acima de 1.0 intensifica o efeito)

    # 2.1) Brilho +10%
    bright_enhancer = ImageEnhance.Brightness(img)
    img_bright = bright_enhancer.enhance(1.1)

    # 2.2) Contraste +15%
    contrast_enhancer = ImageEnhance.Contrast(img_bright)
    img_contrast = contrast_enhancer.enhance(1.15)

    # 2.3) Saturação +10%
    color_enhancer = ImageEnhance.Color(img_contrast)
    img_color = color_enhancer.enhance(1.1)

    # 2.4) Nitidez +20%
    sharp_enhancer = ImageEnhance.Sharpness(img_color)
    final_img = sharp_enhancer.enhance(1.2)

    # 3) INSERIR TEXTO
    #    - Aqui usamos "ImageFont.load_default()" por simplicidade.
    #    - Se quiser fonte TTF, faça: ImageFont.truetype("arial.ttf", 24)
    draw = ImageDraw.Draw(final_img)
    texto = "Cute Shiba!"
    font = ImageFont.truetype("arial.ttf",30)

    # Use textbbox para descobrir o retângulo (x1, y1, x2, y2)
    bbox = draw.textbbox((0, 0), texto, font=font)
    texto_largura = bbox[2] - bbox[0]
    texto_altura  = bbox[3] - bbox[1]

    # Definimos a posição (canto inferior direito, com 10 px de margem)
    x_pos = final_img.width - texto_largura - 10
    y_pos = final_img.height - texto_altura - 10

    # Desenha o texto em branco
    draw.text((x_pos, y_pos), texto, fill="white", font=font)

    # 4) SALVAR A IMAGEM RESULTANTE
    final_img.save(output_path)


if __name__ == "__main__":
    editar_imagem_dog("dog.png", "dog_editado.png")
