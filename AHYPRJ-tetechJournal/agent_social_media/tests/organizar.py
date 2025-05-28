import os
import shutil
import re

# Diretório raiz do projeto
ROOT_DIR = os.getcwd()
FLOW_DIR = os.path.join(ROOT_DIR, "flow")

# Mapeamento dos arquivos de flow para seus novos nomes e pastas
flow_files = {
    "F001_retrieveMessageFromWhatsapp.py": ("core/social_media/", "whatsapp_notifier.py"),
    "F002_decodeAndSaveImage.py": ("core/image_processing/", "image_decode_save.py"),
    "F003_applyFiltersAndBorder.py": ("core/image_processing/", "filter.py"),
    "F004_uploadImageToCloud.py": ("infra/imgur/", "imgur_service.py"),
    "F005_generateImageDescription.py": ("core/ai/", "describe_image.py"),
    "F006_generateInstagramCaption.py": ("core/ai/", "generate_caption.py"),
    "F007_postToInstagram.py": ("core/social_media/", "instagram_post.py"),
    "F008_notifyWhatsappGroup.py": ("core/social_media/", "whatsapp_notifier.py"),
    "F009_cleanupTempFiles.py": ("core/tasks/", "cleanup.py"),
}

# Mover e renomear arquivos da flow/
for old_name, (new_folder, new_name) in flow_files.items():
    src = os.path.join(FLOW_DIR, old_name)
    dest = os.path.join(ROOT_DIR, new_folder, new_name)

    if os.path.exists(src):  # Verifica se o arquivo existe antes de mover
        shutil.move(src, dest)
        print(f"✅ Movido e renomeado: {old_name} → {new_folder}{new_name}")
    else:
        print(f"⚠️ Arquivo não encontrado: {old_name}")

# Atualizar imports nos arquivos Python
def update_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Substituições para os novos caminhos dos arquivos do fluxo
    replacements = {
        r"\bfrom F001_retrieveMessageFromWhatsapp import": "from core.social_media.whatsapp_notifier import",
        r"\bfrom F002_decodeAndSaveImage import": "from core.image_processing.image_decode_save import",
        r"\bfrom F003_applyFiltersAndBorder import": "from core.image_processing.filter import",
        r"\bfrom F004_uploadImageToCloud import": "from infra.imgur.imgur_service import",
        r"\bfrom F005_generateImageDescription import": "from core.ai.describe_image import",
        r"\bfrom F006_generateInstagramCaption import": "from core.ai.generate_caption import",
        r"\bfrom F007_postToInstagram import": "from core.social_media.instagram_post import",
        r"\bfrom F008_notifyWhatsappGroup import": "from core.social_media.whatsapp_notifier import",
        r"\bfrom F009_cleanupTempFiles import": "from core.tasks.cleanup import",
    }

    # Aplicar as substituições
    for old, new in replacements.items():
        content = re.sub(old, new, content)

    # Sobrescrever o arquivo atualizado
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

# Atualizar todos os arquivos Python no projeto
for root, _, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith(".py") and file not in ["mover_e_renomear_flow.py"]:
            file_path = os.path.join(root, file)
            update_imports(file_path)
            print(f"🔄 Atualizado: {file}")

print("\n✅ Arquivos da pasta `flow/` renomeados, movidos e imports corrigidos! 🚀")
