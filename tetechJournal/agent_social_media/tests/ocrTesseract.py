from core.image_processing import OCRtesseract

# Caminho para o executável do Tesseract (necessário apenas no Windows)
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Modifique conforme necessário

# Caminho da imagem para OCR
image_path = "./testText.png"  # Substitua pelo caminho real

extractor = OCRtesseract.ImageTextExtractor(tesseract_path)
extracted_text = extractor.extract_text(image_path, lang="por")  # Mudar para "eng" se for inglês

print("\n📜 Texto extraído da imagem:\n", extracted_text)
