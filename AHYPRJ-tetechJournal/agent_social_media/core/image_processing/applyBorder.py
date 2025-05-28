from PIL import Image


class ImageWithBorder:
    @staticmethod
    def create_bordered_image(image_path, border_path, output_path, target_size=(1080, 1080)):
        """
        Cria a imagem com a borda e salva no caminho especificado.

        Args:
            image_path (str): Caminho da imagem base.
            border_path (str): Caminho da borda.
            output_path (str): Caminho para salvar a imagem resultante.
            target_size (tuple): Dimensão alvo para o corte central (largura, altura).
        Returns:
            str: Caminho da imagem resultante.
        """
        # Abrir a imagem e a borda
        image = Image.open(image_path)
        border = Image.open(border_path)
        
        # Calcular o corte central da imagem
        width, height = image.size
        left = (width - target_size[0]) // 2
        top = (height - target_size[1]) // 2
        right = left + target_size[0]
        bottom = top + target_size[1]
        cropped_image = image.crop((left, top, right, bottom))
        
        # Redimensionar a imagem para coincidir com a borda
        #resized_image = cropped_image.resize(border.size)
        
        # Colocar a imagem redimensionada sobre a borda
        result = Image.new("RGBA", border.size)
        result.paste(cropped_image, (0, 0))
        result.paste(border, (0, 0), mask=border)
        
        # Salvar a imagem resultante
        result.save(output_path)
        return output_path


