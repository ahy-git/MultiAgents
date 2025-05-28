from PIL import Image, ImageDraw, ImageFont, ImageColor

class ImageTextOverlay:
    @staticmethod
    def add_text_to_image(image_path, text, output_path, position=None, font_size=None, font_color="white",
                          outline_color="black", font_path="arial.ttf", 
                          box_enabled=False, box_color="black", box_opacity=150,
                          box_padding=20, box_border_thickness=5, box_border_color="white", 
                          box_roundness=10):
        """
        Adiciona um texto sobre uma imagem com fundo opcional.
        
        Args:
            image_path (str): Caminho da imagem de entrada.
            text (str): Texto a ser inserido na imagem.
            output_path (str): Caminho para salvar a imagem modificada.
            position (tuple, optional): Posição (x, y) onde o texto será inserido. Se None, centraliza.
            font_size (int, optional): Tamanho da fonte. Se None, calcula automaticamente.
            font_color (str): Cor do texto.
            outline_color (str): Cor do contorno do texto.
            font_path (str): Caminho para um arquivo de fonte .ttf.
            box_enabled (bool): Ativar fundo para o texto.
            box_color (str): Cor do fundo do texto.
            box_opacity (int): Opacidade da caixa (0-255).
            box_padding (int): Espaçamento interno da caixa de fundo.
            box_border_thickness (int): Espessura da borda da caixa.
            box_border_color (str): Cor da borda da caixa.
            box_roundness (int): Raio da borda para arredondamento.

        Returns:
            str: Caminho da imagem salva.
        """
        # Carregar a imagem
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # Ajustar tamanho da fonte automaticamente se não for definido
        if font_size is None:
            font_size = int(height * 0.1)  # 10% da altura da imagem como tamanho do texto

        # Carregar a fonte
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            raise Exception(f"Erro ao carregar a fonte '{font_path}'. Verifique o caminho.")

        # Medir tamanho do texto
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]

        # Ajustar posição se não for especificada (centralizar)
        if position is None:
            position = ((width - text_width) // 2, (height - text_height) // 2)
       
        # ✅ Fix for RGBA `box_color` parsing
        if isinstance(box_color, str) and box_color.startswith("rgba"):
            try:
                rgba_values = [float(v) if i == 3 else int(v) for i, v in enumerate(box_color[5:-1].split(","))]
                box_color = tuple(int(rgba_values[i]) if i < 3 else int(rgba_values[i] * 255) for i in range(4))
            except Exception as e:
                print(f"⚠️ Error parsing box_color `{box_color}`: {e}. Defaulting to black.")
                box_color = (0, 0, 0, 180)  # Default to black with opacity

        else:
            try:
                box_color = (*ImageColor.getrgb(box_color), box_opacity)  # Convert to (R, G, B, A)
            except ValueError:
                print(f"⚠️ Invalid box_color `{box_color}`, defaulting to black.")
                box_color = (0, 0, 0, box_opacity)

        # ✅ Ensure box color is an RGBA tuple
        if len(box_color) == 3:
            box_color = (*box_color, box_opacity)
        # Definir coordenadas da caixa de fundo
        
        
        if box_enabled:
            box_x1 = position[0] - box_padding
            box_y1 = position[1] - box_padding
            box_x2 = position[0] + text_width + box_padding
            box_y2 = position[1] + text_height + box_padding

            # Criar um fundo semi-transparente
            box_overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
            box_draw = ImageDraw.Draw(box_overlay)
 
            # Desenhar a caixa arredondada
            box_draw.rounded_rectangle(
                [(box_x1, box_y1), (box_x2, box_y2)], 
                fill=box_color if isinstance(box_color, tuple) else (*ImageColor.getrgb(box_color), box_opacity),
                outline=box_border_color,
                width=box_border_thickness,
                radius=box_roundness
            )

            # Aplicar a caixa de fundo à imagem original
            image = Image.alpha_composite(image.convert("RGBA"), box_overlay)

        # Criar objeto de desenho novamente após modificações
        draw = ImageDraw.Draw(image)

        # Desenhar contorno do texto para legibilidade
        for offset in [-2, -1, 0, 1, 2]:
            draw.text((position[0] + offset, position[1]), text, font=font, fill=outline_color)
            draw.text((position[0] - offset, position[1]), text, font=font, fill=outline_color)
            draw.text((position[0], position[1] + offset), text, font=font, fill=outline_color)
            draw.text((position[0], position[1] - offset), text, font=font, fill=outline_color)

        # Desenhar o texto principal por cima
        draw.text(position, text, font=font, fill=font_color)

        # Converter para RGB se for RGBA (para evitar problemas ao salvar)
        if image.mode == "RGBA":
            image = image.convert("RGB")

        # Salvar a nova imagem
        image.save(output_path)

        return output_path

