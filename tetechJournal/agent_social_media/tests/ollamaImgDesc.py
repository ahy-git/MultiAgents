from core.ai.describe_image_ollama import OllamaImageDescriber    
    
image_path = "./testText.png"  # Substitua pelo caminho real da imagem
describer = OllamaImageDescriber()
description = describer.describe_image(image_path)
print("Descrição da imagem:", description)