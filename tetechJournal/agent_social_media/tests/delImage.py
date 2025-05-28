from infra.imgur.imgur_service import ImageUploader

def delete_imgur_image(deletehash):
    """
    Deleta uma imagem do Imgur usando o deletehash fornecido.
    """
    uploader = ImageUploader()
    success = uploader.delete_image(deletehash)

    if success:
        print(f"✅ Imagem removida do Imgur: {deletehash}")
    else:
        print(f"❌ Falha ao deletar a imagem: {deletehash}")

if __name__ == "__main__":
    # Insira o deletehash da imagem que deseja remover
    deletehash = input("🔴 Digite o deletehash da imagem para deletar: ").strip()
    
    if deletehash:
        delete_imgur_image(deletehash)
    else:
        print("⚠️ Nenhum deletehash fornecido. Operação cancelada.")
