from core.ai.generate_image import generate_image
import os
import itertools


# Diretório de saída
OUTPUT_DIR = "./tests/genimg"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Feitos: "stable_diffusion_v1.5", "kandinsky_2.2", deepfloyd nao roda sem GPU
# to add: 
# stabilityai/stable-diffusion-3.5-medium
# stabilityai/stable-diffusion-3.5-large
# stabilityai/stable-video-diffusion-img2vid-xt
# stabilityai/stable-video-diffusion-img2vid-xt-1-1
# stabilityai/stable-diffusion-3.5-large-turbo
# stabilityai/stable-diffusion-xl-refiner-1.0
# tencent/Hunyuan3D-2
# For best performance on CPU: CompVis/stable-diffusion-v1-4
# For more detailed images (but slower): stabilityai/stable-diffusion-2-1
# If you really want SDXL (very slow on CPU): stabilityai/stable-diffusion-xl-base-1.0

# Parâmetros a serem iterados
MODEL_NAMES = [ "deepfloyd_if", "pixart_alpha", "invokeai"]
NUM_INFERENCE_STEPS = [10, 30, 50]
GUIDANCE_SCALES = [3, 5, 7.5, 8, 10]
IMAGE_SIZE = (512, 512)
PROMPT="""
A cute and cheerful digital illustration of Tete, a plump pink plush pig with an inverted heart-shaped nose and no ears, wearing a captain's hat. 
Tete is standing happily next to a friendly plush llama and a plush whale. The scene is colorful, warm, and inviting, with soft lighting and a whimsical atmosphere. 
The illustration is in a highly detailed, 2D cartoon style, with smooth shading and soft textures. Soft pastel colors, adorable expressions, charming and heartwarming, cozy ambiance, children's storybook style.
natural light, 35mm illustration, film, professional, 4k, highly detailed, golden hour lighting. Depth of field F2. Rule of Thirds Composition.
""",
NEG_PROMPT="""
    malformed, extra limbs, poorly drawn anatomy, badly drawn, extra legs, low resolution, blurry, watermark, text, censored, deformed, 
    bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, 
    disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, 
    low quality, mutation, poorly drawn, fused hand, missing hand, disappearing arms, disappearing legs, missing fingers, fused fingers, 
    abnormal proportions, noisy, blurry, soft, deformed, ugly, hyperrealistic, photorealistic, uncanny, 3D render, realistic lighting.
    """

# Gerar todas as combinações possíveis
combinations = list(itertools.product(MODEL_NAMES, NUM_INFERENCE_STEPS, GUIDANCE_SCALES))

# Verificar progresso e retomar de onde parou
completed_images = set(os.listdir(OUTPUT_DIR))  # Arquivos já gerados

for model_name, num_steps, guidance in combinations:
    safe_model_name = model_name.replace(".", "_").replace("/", "_")
    safe_guidandace= str(guidance).replace(".", "_").replace("/", "_")
    img_name_2 = f"img_{safe_model_name}_{num_steps}_{safe_guidandace}"
    image_filename = f"imagem_{safe_model_name}_{num_steps}steps_{guidance}guidance.png"
    labeled_image_filename = f"imagem_{safe_model_name}_{num_steps}steps_{guidance}guidance_label.png"

    image_path = os.path.join(OUTPUT_DIR, image_filename)
    labeled_image_path = os.path.join(OUTPUT_DIR, labeled_image_filename)

    # Se a imagem já foi gerada, pula para a próxima
    if image_filename in completed_images or labeled_image_filename in completed_images:
        print(f"⏩ Pulando {image_filename}, já gerado.")
        continue
    
       # Se a imagem já foi gerada, pula para a próxima
    if img_name_2 in completed_images or labeled_image_filename in completed_images:
        print(f"⏩ Pulando img_name_2 {img_name_2}, já gerado.")
        continue
    
    try:
        # Gerar imagem com os parâmetros atuais
        print(f"🎨 Gerando imagem: {image_filename} ({model_name}, {num_steps} steps, {guidance} guidance)")
        image, labeled_image = generate_image(
            output_dir=OUTPUT_DIR,
            model_name=model_name,
            num_inference_steps=num_steps,
            guidance_scale=guidance,
            image_size=IMAGE_SIZE,
            prompt=PROMPT,
            negative_prompt=NEG_PROMPT
        )

        print(f"✅ Imagem salva em: {image}")
        print(f"✅ Imagem com legenda salva em: {labeled_image}")

        # Adicionar ao conjunto de concluídos para evitar retrabalho
        completed_images.add(image_filename)
        completed_images.add(labeled_image_filename)

    except Exception as e:
        print(f"❌ Erro ao gerar {image_filename}: {e}")
        print("⚠️ Continuando para a próxima configuração...")

    # # Remover arquivos gerados para liberar espaço
    # if os.path.exists(image_path):
    #     os.remove(image_path)
    #     print(f"🗑️ Imagem deletada: {image_path}")
    # else:
    #     print(f"⚠️ Arquivo não encontrado: {image_path}")
    # if os.path.exists(labeled_image_path):
    #     os.remove(labeled_image_path)
    #     print(f"🗑️ Imagem com legenda deletada: {labeled_image_path}")
    # else:
    #     print(f"⚠️ Arquivo não encontrado: {labeled_image_path}")

print("🚀 Todas as combinações foram processadas!")
