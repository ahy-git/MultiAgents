from flow.F004_uploadImageToCloud import ImageUploader

# Caminho da imagem local
image_path = "assets/oi.png"  # Substitua pelo caminho correto da sua imagem

# Criar uma instância do uploader e fazer o upload
uploader = ImageUploader()
response = uploader.upload_from_path(image_path)

# Exibir o link gerado
if response:
    print(f"✅ Imagem enviada com sucesso: {response['url']}")
else:
    print("❌ Falha no upload para Imgur.")
