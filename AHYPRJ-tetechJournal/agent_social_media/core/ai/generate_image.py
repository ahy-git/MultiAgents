import torch
import time
import os
from diffusers import StableDiffusionPipeline, AutoPipelineForText2Image, DiffusionPipeline
from transformers import AutoProcessor, AutoModel
from PIL import Image
# Importação da função de overlay
from core.image_processing.textOverlay import ImageTextOverlay
from huggingface_hub import login
import os
from utils.helper import load_env
import requests
load_env()

# HuggingFace Login for models
HF_API_KEY = os.getenv('HF_API_KEY')  # Replace with your actual token



# Lista de modelos disponíveis
MODELS = {
    "stable_diffusion_v1.5": "runwayml/stable-diffusion-v1-5",
    "kandinsky_2.2": "kandinsky-community/kandinsky-2-2-decoder",
    "deepfloyd_if": "DeepFloyd/IF-I-M-v1.0",
    "pixart_alpha": "PixArt-alpha/PixArt-XL-2-1024-MS",
    "invokeai": "InvokeAI/Xinsir-SDXL_Controlnet_Union"
}

# Definir dispositivo de execução
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Corrigido para suportar CPU
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


def generate_image(
    output_dir="./tests/genimg",
    model_name="stable_diffusion_v1.5",
    num_inference_steps=1,
    guidance_scale=7.5,
    image_size=(512, 512),
    prompt="""
A cute and cheerful digital illustration of Tete, a plump pink plush pig with an inverted heart-shaped nose and no ears, wearing a captain's hat. 
Tete is standing happily next to a friendly plush llama and a plush whale. The scene is colorful, warm, and inviting, with soft lighting and a whimsical atmosphere. 
The illustration is in a highly detailed, 2D cartoon style, with smooth shading and soft textures. Soft pastel colors, adorable expressions, charming and heartwarming, cozy ambiance, children's storybook style.
natural light, 35mm illustration, film, professional, 4k, highly detailed, golden hour lighting. Depth of field F2. Rule of Thirds Composition.
""",
    negative_prompt="""
    malformed, extra limbs, poorly drawn anatomy, badly drawn, extra legs, low resolution, blurry, watermark, text, censored, deformed, 
    bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, 
    disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, 
    low quality, mutation, poorly drawn, fused hand, missing hand, disappearing arms, disappearing legs, missing fingers, fused fingers, 
    abnormal proportions, noisy, blurry, soft, deformed, ugly, hyperrealistic, photorealistic, uncanny, 3D render, realistic lighting.
    """
):
    """
    Gera uma imagem com IA usando o modelo especificado e adiciona legenda com informações.

    Args:
        output_dir (str): Diretório para salvar a imagem.
        model_name (str): Nome do modelo a ser usado.
        num_inference_steps (int): Número de passos de inferência.
        guidance_scale (float): Escala de guidance.
        image_size (tuple): Dimensão da imagem (largura, altura).
        prompt (str): Texto de entrada para geração.

    Returns:
        tuple: (caminho da imagem gerada, caminho da imagem com legenda).
    """

    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Função para carregar o modelo
    def load_model(model_name):
        print(f"🖼️ Carregando modelo: {model_name}")
        if model_name.startswith("stable_diffusion"):
            return StableDiffusionPipeline.from_pretrained(MODELS[model_name]).to(DEVICE)
        elif model_name == "kandinsky_2.2":
            login(HF_API_KEY)
            return AutoPipelineForText2Image.from_pretrained(
                MODELS[model_name], torch_dtype=TORCH_DTYPE
            ).to(DEVICE)           
                    
        elif model_name == "pixart_alpha":
            from diffusers import DiffusionPipeline
            login(HF_API_KEY)
            return DiffusionPipeline.from_pretrained(
                MODELS[model_name], torch_dtype=TORCH_DTYPE
            ).to(DEVICE)
            
        elif model_name == "invokeai":
            from diffusers import DiffusionPipeline
            login(HF_API_KEY)
            return DiffusionPipeline.from_pretrained(
                MODELS[model_name], torch_dtype=TORCH_DTYPE
            ).to(DEVICE)
        else:
            raise ValueError(f"Modelo {model_name} não suportado.")

    # Carregar modelo selecionado
    pipe = load_model(model_name)

    # Medir tempo de execução
    start_time = time.time()

    # Gerar imagem
    if model_name == "deepfloyd_if":
        processor = pipe[1]
        model = pipe[0]
        inputs = processor(text=prompt, return_tensors="pt").to(DEVICE)
        image = model.generate(**inputs, guidance_scale=guidance_scale)
        image = processor.decode(image[0])

    elif model_name == "kandinsky_2.2":
        image = pipe(prompt, negative_prompt,
                     height=image_size[1], width=image_size[0]).images[0]
    else:
        image = pipe(prompt, negative_prompt, num_inference_steps=num_inference_steps,
                     guidance_scale=guidance_scale).images[0]

    # Calcular tempo decorrido e formatar como hh:mm:ss
    elapsed_time = int(time.time() - start_time)
    elapsed_hours = elapsed_time // 3600
    elapsed_minutes = (elapsed_time % 3600) // 60
    elapsed_seconds = elapsed_time % 60
    formatted_time = f"{elapsed_hours:02}h{elapsed_minutes:02}m{elapsed_seconds:02}s"

    # Criar string da configuração usada
    config_text_l1 = f"{model_name} | {DEVICE} | {num_inference_steps} steps"
    config_text_l2 = f"{guidance_scale} guidance | {image_size[0]}x{image_size[1]} px "
    final_text = f"""TimeElpsd: {formatted_time}\n
{config_text_l1}\n
{config_text_l2}
              """

    # Salvar imagem
    safe_model_name = model_name.replace(".", "_").replace("/", "_")
    safe_guidance_scale = str(guidance_scale).replace(
        ".", "_").replace("/", "_")
    inference_str = str(num_inference_steps)
    img_name = f"{safe_model_name}_{inference_str}_{safe_guidance_scale}"
    image_path = os.path.join(output_dir, f"img_{img_name}.png")
    image.save(image_path)

    # Gerar legenda na imagem
    output_image_path = os.path.join(output_dir, f"img_{img_name}_label.png")
    ImageTextOverlay.add_text_to_image(
        image_path, final_text, output_image_path,
        position=(10, image_size[1] - 120),  # Posição na parte inferior
        font_size=16, font_color="white", outline_color="black",
        box_enabled=True, box_color="blue", box_opacity=80,
        box_padding=30, box_border_thickness=5, box_border_color="black",
        box_roundness=30
    )

    print(f"✅ Imagem gerada com sucesso! ({image_path})")
    print(f"✅ Imagem c/ legenda salva em: {output_image_path}")
    print(f"⏳ Tempo decorrido: {formatted_time}")
    print(f"📌 Configuração usada: {config_text_l1} {config_text_l2}")

    return image_path, output_image_path
