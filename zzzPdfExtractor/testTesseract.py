import pytesseract
from PIL import Image

# Defina o caminho do Tesseract manualmente
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Teste com uma imagem real
image_path = "teste.jpg"  # Troque por uma imagem válida
image = Image.open(image_path)
text = pytesseract.image_to_string(image)

print("Texto extraído:\n", text)
