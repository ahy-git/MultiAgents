import torch
import time
import os
from diffusers import StableDiffusionPipeline, StableDiffusionUpscalePipeline, EulerAncestralDiscreteScheduler, DPMSolverMultistepScheduler, LMSDiscreteScheduler, DDIMScheduler, HeunDiscreteScheduler
from transformers import AutoProcessor, AutoModel
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

# Lista de modelos disponíveis
MODELS = {
    "stablediffusion15": "runwayml/stable-diffusion-v1-5",
    "stablediffusion21": "stabilityai/stable-diffusion-2-1",
    "stablediffusion35m" :"stabilityai/stable-diffusion-3.5-medium",
    "stablediffusion35l" :"stabilityai/stable-diffusion-3.5-large",
    "tencent" : "tencent/Hunyuan3D-2",
    "deliberate2" : "Yntec/Deliberate2", #realistic
    "sdvalardeliberate2" : "SdValar/deliberate2", #realistic
    "anythingv5":"Yntec/AnythingV5-768", #anime
    "realisticvision":"Yntec/realistic-vision-v13"
    # :"stabilityai/stable-diffusion-3.5-large-turbo"
    # :"stabilityai/stable-diffusion-xl-refiner-1.0"
    # :"stabilityai/stable-video-diffusion-img2vid-xt"
    # :"stabilityai/stable-video-diffusion-img2vid-xt-1-1"

}

# Lista de Samplers disponíveis
SAMPLERS = {
    "euler_a": EulerAncestralDiscreteScheduler,
    "dpmpp_2m_karras": DPMSolverMultistepScheduler,
    "lms": LMSDiscreteScheduler,
    "ddim": DDIMScheduler,
    "heun": HeunDiscreteScheduler,
}

#  Parâmetros ajustáveis
OUTPUT_DIR = "./tests/genimg"
MODEL_NAME = "deliberate2"  # Modelo escolhido
SAMPLER_NAME = "euler_a"  # Sampler escolhido (Altere para testar outros)
NUM_INFERENCE_STEPS = 30  # Passos de inferência
GUIDANCE_SCALE = 9  # Ajusta a fidelidade ao prompt (3-10 recomendado)
IMAGE_SIZE = (512, 910)  # Alterar para (768, 768) ou mais se necessário
SEED = 42  # Defina um número para gerar imagens reprodutíveis ou None para aleatório
ENABLE_UPSCALING = False  # Ativar ou desativar o upscaling
UPSCALER_MODEL = "stabilityai/stable-diffusion-x4-upscaler"  # Modelo de upscaling
# PROMPT = """cute pink happy round-shaped pig with small legs. her name is Tete, The scene is colorful, warm, and inviting, with soft lighting and a whimsical atmosphere. 
#  The illustration is in a highly detailed, 3D cartoon style, with smooth shading and soft textures. Soft pastel colors, adorable expressions, charming and heartwarming, cozy ambiance, anime style.
# natural light, 35mm illustration, film, professional, 4k, highly detailed, golden hour lighting. Depth of field F2. Rule of Thirds Composition."""
# NEG_PROMPT = "dog, cat, other animal, malformed, big ears, big nose"
PROMPT = """
A cute and cheerful digital illustration of Tete, a plump pink plush pig with, small eyes, an small inverted heart-shaped nose and no ears, wearing a captain's hat. 
Tete is standing happily next to a friendly plush llama and a plush whale. The scene is colorful, warm, and inviting, with soft lighting and a whimsical atmosphere. 
The illustration is in a highly detailed, 3D cartoon style, with smooth shading and soft textures. Soft pastel colors, adorable expressions, charming and heartwarming, cozy ambiance, anime style.
natural light, 35mm illustration, film, professional, 4k, highly detailed, golden hour lighting. Depth of field F2. Rule of Thirds Composition.
"""

NEG_PROMPT = """
malformed, extra limbs, poorly drawn anatomy, badly drawn, extra legs, low resolution, blurry, watermark, text, censored, deformed, 
bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, 
disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, 
low quality, mutation, poorly drawn, fused hand, missing hand, disappearing arms, disappearing legs, missing fingers, fused fingers, 
abnormal proportions, noisy, blurry, soft, no face deformed, ugly, hyperrealistic, photorealistic, uncanny, 3D render, realistic lighting.
"""

# Criar diretório de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Definir dispositivo de execução
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Função para carregar o modelo com o sampler correto
def load_model(model_name, sampler_name):
    print(f"🖼️ Carregando modelo: {model_name} com sampler: {sampler_name}")
    
    # Carregar pipeline do modelo
    pipe = StableDiffusionPipeline.from_pretrained(MODELS[model_name], torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32).to(DEVICE)

    # Configurar sampler
    if sampler_name in SAMPLERS:
        pipe.scheduler = SAMPLERS[sampler_name].from_config(pipe.scheduler.config)
        print(f"✅ Sampler '{sampler_name}' aplicado com sucesso!")
    else:
        print(f"⚠️ Sampler '{sampler_name}' não encontrado. Usando o padrão do modelo.")

    return pipe

# Função para carregar o upscaler
def load_upscaler():
    print("🔼 Carregando modelo de upscaling...")
    upscaler = StableDiffusionUpscalePipeline.from_pretrained(UPSCALER_MODEL, torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32).to(DEVICE)
    print("✅ Upscaler carregado com sucesso!")
    return upscaler

# Função para encontrar o próximo nome de arquivo disponível
def get_next_image_path(suffix=""):
    base_filename = f"imagem_{MODEL_NAME}_{SAMPLER_NAME}{suffix}"
    count = 1

    while True:
        image_filename = f"{base_filename}_{count:03}.png"
        image_path = os.path.join(OUTPUT_DIR, image_filename)

        if not os.path.exists(image_path):
            return image_path  # Retorna o primeiro nome disponível
        
        count += 1  # Se já existe, tenta o próximo número

# Carregar modelo e sampler selecionado
pipe = load_model(MODEL_NAME, SAMPLER_NAME)

# Definir seed
if SEED is not None:
    generator = torch.manual_seed(SEED)
    print(f"🎲 Usando Seed fixa: {SEED}")
else:
    generator = None
    print("🎲 Usando Seed aleatória!")

# Medir tempo de execução
start_time = time.time()

# Gerar imagem com negative prompts e sampler configurado
image = pipe(
    prompt=PROMPT,
    negative_prompt=NEG_PROMPT,
    num_inference_steps=NUM_INFERENCE_STEPS,
    guidance_scale=GUIDANCE_SCALE,
    generator=generator
).images[0]

# Calcular tempo decorrido
elapsed_time = int(time.time() - start_time)
formatted_time = f"{elapsed_time // 3600:02}h{(elapsed_time % 3600) // 60:02}m{elapsed_time % 60:02}s"

# Criar string da configuração usada
config_text = f"{MODEL_NAME} | {DEVICE} | {NUM_INFERENCE_STEPS} steps | Sampler: {SAMPLER_NAME}\n"
config_text += f"Seed: {SEED if SEED is not None else 'Random'} | {GUIDANCE_SCALE} guidance | {IMAGE_SIZE[0]}x{IMAGE_SIZE[1]} px\n"
config_text += f"Time Elapsed: {formatted_time}"

# Obter o próximo nome disponível para a imagem
IMAGE_PATH = get_next_image_path()
image.save(IMAGE_PATH)

print(f"✅ Imagem gerada por AI com sucesso! ({IMAGE_PATH})")
print(f"⏳ Tempo decorrido: {formatted_time}")
print(f"📌 Configuração usada: {config_text}")

# Aplicar Upscaling se ativado
if ENABLE_UPSCALING:
    upscaler = load_upscaler()
    upscaled_image = upscaler(prompt=PROMPT, image=image).images[0]
    UPSCALED_IMAGE_PATH = get_next_image_path("_upscaled")
    upscaled_image.save(UPSCALED_IMAGE_PATH)
    print(f"🔼 Imagem com upscaling salva: {UPSCALED_IMAGE_PATH}")