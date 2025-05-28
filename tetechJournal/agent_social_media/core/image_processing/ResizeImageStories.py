from PIL import Image
import os
import shutil

class EditImageStories:
    """
    Classe para processar imagens e transformá-las em formato de Stories para Instagram.
    """

    @staticmethod
    def is_nine_sixteen_aspect_ratio(width, height):
        """
        Verifica se a imagem possui a proporção de 9:16.
        """
        aspect_ratio = width / height
        expected_ratio = 9 / 16
        return abs(aspect_ratio - expected_ratio) < 0.01  # Tolerância para pequenas variações

    @staticmethod
    def transform_to_story_format(image_path, output_path):
        """
        Transforma a imagem para o formato adequado de Stories (1080x1920).
        Se já existir um arquivo com sufixo _rszd, retorna esse arquivo.
        Se a imagem já for 1080x1920, cria uma cópia com _rszd.

        :param image_path: Caminho da imagem original.
        :param output_path: Caminho para salvar a imagem transformada.
        :return: Caminho da imagem transformada.
        """

        # Normalize paths
        image_path = os.path.abspath(image_path).replace("\\", "/")
        output_path = os.path.abspath(output_path).replace("\\", "/")

        # Get folder and filename
        folder_path = os.path.dirname(image_path)
        base_name, ext = os.path.splitext(os.path.basename(image_path))
        resized_image_path = os.path.join(folder_path, f"{base_name}_rszd{ext}")

        # Check if a resized version already exists
        if os.path.exists(resized_image_path):
            print(f"✅ Resized image already exists: {resized_image_path}")
            return resized_image_path  # Return existing resized file

        # Ensure the input file exists
        if not os.path.exists(image_path):
            print(f"❌ Error: Input image not found at {image_path}")
            return None

        try:
            # Standard Story size
            target_width, target_height = (1080, 1920)

            # Open the image and check its size
            image = Image.open(image_path)
            width, height = image.size


            if EditImageStories.is_nine_sixteen_aspect_ratio(width, height):
                print(f"✅ Image is already in 9:16 aspect ratio. Creating a copy with `_rszd` suffix...")
                shutil.copy(image_path, resized_image_path)
                print(f"📂 Copied image saved at: {resized_image_path}")
                return resized_image_path, width, height

            print(f"🔄 Resizing image to {target_width}x{target_height} while maintaining proportions...")


            # Convert image to RGBA if needed
            image = image.convert("RGBA")

            # Resize while maintaining proportions
            image.thumbnail((target_width, target_height), Image.LANCZOS)

            # Create a white background
            story_image = Image.new("RGBA", (target_width, target_height), (242, 196, 255, 255))

            # Center the image on the background
            x_offset = (target_width - image.size[0]) // 2
            y_offset = (target_height - image.size[1]) // 2
            story_image.paste(image, (x_offset, y_offset), mask=image)

            # Save transformed image with `_rszd` suffix
            story_image.save(resized_image_path, format="PNG")

            print(f"✅ Image successfully resized and saved at: {resized_image_path}")
            return resized_image_path,1080,1920

        except Exception as e:
            print(f"❌ Error processing image: {e}")
            return None
