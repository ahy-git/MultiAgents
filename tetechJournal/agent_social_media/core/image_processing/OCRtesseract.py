import pytesseract
from PIL import Image
import os


class ImageTextExtractor:
    def __init__(self, tesseract_path=None):
        """
        Inicializa o OCR Tesseract.
        Se um caminho para o executável do Tesseract for fornecido, ele será configurado.
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def extract_text(self, image_path, lang="eng"):
        """
        Lê uma imagem e extrai o texto usando Tesseract OCR.

        Args:
            image_path (str): Caminho da imagem.
            lang (str): Código do idioma para OCR (padrão: "eng" para inglês).

        Returns:
            str: Texto extraído da imagem.
        """
        if not os.path.exists(image_path):
            return f"❌ Erro: Arquivo '{image_path}' não encontrado."

        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            return f"⚠️ Erro ao processar imagem: {e}"

