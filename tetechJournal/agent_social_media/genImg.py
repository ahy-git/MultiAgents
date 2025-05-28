import torch
import time
import os
from diffusers import StableDiffusionPipeline, KandinskyPipeline
from transformers import AutoProcessor, AutoModel
from PIL import Image
from core.image_processing.textOverlay import ImageTextOverlay  # Importação da função de overlay


# Lista de modelos disponíveis
MODELS = {
    "stable_diffusion_v1.5": "runwayml/stable-diffusion-v1-5",
    "kandinsky_2.2": "kandinsky-community/kandinsky-2-2-decoder",
    "deepfloyd_if": "DeepFloyd/IF-I-M-v1.0",
    "pixart_alpha": "pixart-alpha/PixArt-α",
    "invokeai": "invokeai/stable-diffusion-2.1",
    "comfyui": None  # ComfyUI requer execução separada
}

# Parâmetros ajustáveis
OUTPUT_DIR = "./tests/genimg"
MODEL_NAME = "stable_diffusion_v1.5"  # Altere para testar outro modelo
NUM_INFERENCE_STEPS = 1  # Passos de inferência (quanto maior, melhor qualidade, mas mais lento)
GUIDANCE_SCALE = 7.5  # Ajusta a fidelidade ao prompt (3-10 recomendado)
IMAGE_SIZE = (512, 910)  # Alterar para (768, 768) ou mais se necessário
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


# Criar diretório de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Definir dispositivo de execução
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Função para carregar o modelo
def load_model(model_name):
    print(f"🖼️ Carregando modelo: {model_name}")
    if model_name.startswith("stable_diffusion"):
        return StableDiffusionPipeline.from_pretrained(MODELS[model_name]).to(DEVICE)
    elif model_name == "kandinsky_2.2":
        return KandinskyPipeline.from_pretrained(MODELS[model_name]).to(DEVICE)
    elif model_name == "deepfloyd_if":
        processor = AutoProcessor.from_pretrained(MODELS[model_name])
        model = AutoModel.from_pretrained(MODELS[model_name]).to(DEVICE)
        return model, processor
    elif model_name == "pixart_alpha":
        return StableDiffusionPipeline.from_pretrained(MODELS[model_name]).to(DEVICE)
    elif model_name == "invokeai":
        return StableDiffusionPipeline.from_pretrained(MODELS[model_name]).to(DEVICE)
    else:
        raise ValueError(f"Modelo {model_name} não suportado.")

# Carregar modelo selecionado
pipe = load_model(MODEL_NAME)

# Medir tempo de execução
start_time = time.time()

# Gerar imagem
if MODEL_NAME == "deepfloyd_if":
    processor = pipe[1]
    model = pipe[0]
    inputs = processor(text=PROMPT, return_tensors="pt").to(DEVICE)
    image = model.generate(**inputs, guidance_scale=GUIDANCE_SCALE)
    image = processor.decode(image[0])
else:
    image = pipe(PROMPT, num_inference_steps=NUM_INFERENCE_STEPS, guidance_scale=GUIDANCE_SCALE).images[0]

# Calcular tempo decorrido e formatar como hh:mm:ss
elapsed_time = int(time.time() - start_time)
elapsed_hours = elapsed_time // 3600
elapsed_minutes = (elapsed_time % 3600) // 60
elapsed_seconds = elapsed_time % 60
formatted_time = f"{elapsed_hours:02}h{elapsed_minutes:02}m{elapsed_seconds:02}s"

# Criar string da configuração usada
config_text_l1 = f"{MODEL_NAME} | {DEVICE} | {NUM_INFERENCE_STEPS} steps"
config_text_l2 = f"{GUIDANCE_SCALE} guidance | {IMAGE_SIZE[0]}x{IMAGE_SIZE[1]} px "
final_text = f"""TimeElpsd: {formatted_time}\n
{config_text_l1}\n
{config_text_l2}
              """

# Definir caminho de saída
IMAGE_PATH = os.path.join(OUTPUT_DIR, f"imagem_{MODEL_NAME}.png")
image.save(IMAGE_PATH)
# Imprimir tempo decorrido e configurações usadas
print(f"✅ Imagem gerada por AI com sucesso! ({IMAGE_PATH})")
print(f"⏳ Tempo decorrido: {formatted_time}")
print(f"📌 Configuração usada: {config_text_l1} {config_text_l2}")


# Gerar Legenda
input_image = IMAGE_PATH
output_image=os.path.join(OUTPUT_DIR, f"imagem_{MODEL_NAME}_label.png")
text_to_add = final_text

ImageTextOverlay.add_text_to_image(
    input_image, text_to_add, output_image,
    position=(10, IMAGE_SIZE[1] - 120), 
    font_size=16, font_color="white", outline_color="black",
    box_enabled=True, box_color="blue", box_opacity=20,
    box_padding=30, box_border_thickness=5, box_border_color="black",
    box_roundness=30
)
print(f"✅ Imagem c/ legenda salva em: {output_image}")






