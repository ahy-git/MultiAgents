from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import glob
from typing import List
from core.ai.story_generation_crew import StoryGenerationCrew
from core.image_processing.ResizeImageStories import EditImageStories
from core.image_processing.textOverlayStories import TextOverlayProcessor
from core.social_media.instagram_post import InstagramPostService
from infra.tasks.postFinalize import finalize_post
from infra.tasks.pendingPosts import get_pending_posts
from infra.imgur.imgur_service import ImageUploader
from PIL import Image
from core.ai.generate_caption import InstagramCaptionCrew
from utils.telegram_notify import notify_telegram

app = FastAPI()

# Define modelo para entrada da API
class PostRequest(BaseModel):
    folder_path: str

@app.post("/process/story")
def process_story(data: PostRequest, background_tasks: BackgroundTasks):
    # ✅ Enfileira a função para rodar em background
    background_tasks.add_task(process_story_logic, data.folder_path)
    return {"status": "started", "message": f"Processing {data.folder_path}"}

def process_story_logic(folder_path: str):
    """
    Automates the full Instagram Story posting process:
    - Checks for `.posted` to avoid reposts.
    - Generates text if `InputsImage.md` does not exist.
    - Resizes image to Instagram Stories format.
    - Adds text overlays, ensuring no overflow.
    - Uploads, posts, and cleans up images.
    """
    try:
        post_folder = folder_path
        print(f"📂 Checking post folder: {post_folder}", flush=True)

        # Step 1️⃣: Check if `.posted` exists
        posted_flag = os.path.join(post_folder, ".posted")
        if os.path.exists(posted_flag):
            return {"message": "✅ Story already posted. Skipping."}

        # Step 1.1️⃣: Check if `InputsImage.md` exists
        input_md = os.path.join(post_folder, "InputsImage.md")
        goto_step5 = os.path.exists(input_md)

        # Step 2️⃣: Find image in folder
        image_extensions = ("*.png", "*.jpg", "*.jpeg", "*.webp")
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(post_folder, ext)))

        if not image_files:
            # raise HTTPException(status_code=404, detail="❌ No image found.")
            print("❌ No image found.", flush=True)
            return #
        input_image_path = image_files[0]
        print(f"✅ Found image: {input_image_path}", flush=True)

        # Step 4️⃣: Define resized image path
        rszd_images = glob.glob(os.path.join(post_folder, "*_rszd.*"))
        resized_image_path = rszd_images[0] if rszd_images else os.path.join(
            post_folder, f"{os.path.splitext(os.path.basename(input_image_path))[0]}_rszd.png"
        )

        if not goto_step5:
            # Step 3️⃣: Run CrewAI story generation
            print("🚀 Running Story Generation CrewAI Pipeline...", flush=True)
            width, height = Image.open(input_image_path).size
            caption_humano = open(glob.glob("*.txt")[0], encoding="utf-8").read().strip() if glob.glob("*.txt") else ""
            crew = StoryGenerationCrew(image_path=input_image_path, output_path=input_md)
            final_output = crew.kickoff(
                image_folder=post_folder,
                image_path=input_image_path,
                caption_text=caption_humano,
                img_width=width,
                img_height=height
            )
            if not final_output:
                # raise HTTPException(status_code=500, detail="❌ Story Generation Failed.")
                print("❌ Story Generation Failed.", flush=True)
                return 
            print(f"✅ Story Generation Completed. Data saved at: {final_output}", flush=True)

            # Step 4️⃣: Resize image
            print(f"🚀 Resizing image for Instagram Stories format...")
            final_image = EditImageStories.transform_to_story_format(input_image_path, resized_image_path)
            if not final_image:
                # raise HTTPException(status_code=500, detail="❌ Failed to resize image.")
                print("❌ Failed to resize image.", flush=True)
                return
            print(f"✅ Image Resized: {final_image}", flush=True)

        # Step 5️⃣: Ensure resized image exists
        if not os.path.exists(resized_image_path):
            print(f"⚠️ Warning: Resized image not found. Using original image instead.")
            resized_image_path = input_image_path

        # Step 5️⃣: Apply text overlay
        processed_image_path = os.path.join(post_folder, "processed_image.png")
        print("🔋️ Adding text overlay to the image...", flush=True)
        final_story_image = TextOverlayProcessor.process_text_overlay(input_md, resized_image_path, processed_image_path)
        if not final_story_image:
            # raise HTTPException(status_code=500, detail="❌ Failed to process text overlay.")
            print("❌ Failed to process text overlay.")
            return
        print(f"✅ Final Story Image Ready: {final_story_image}", flush=True)

        # Step 6️⃣: Upload and post
        imgur_client = ImageUploader()
        imgurVar = imgur_client.upload_from_path(final_story_image)
        if not imgurVar:
            # raise HTTPException(status_code=500, detail="❌ Image upload failed.")
            print("❌ Image upload failed.")
            return
        print(f"✅ Uploaded Image: {imgurVar['url']}", flush=True)

        insta_service = InstagramPostService()
        story_id = insta_service.post_story(imgurVar["url"])

        if story_id:
            print(f"✅ Story successfully posted! ID: {story_id}", flush=True)
            finalize_post(post_folder, story_id, imgur_client, imgurVar)
            return {"message": "✅ Story posted.", "story_id": story_id}
        else:
            # raise HTTPException(status_code=500, detail="❌ Failed to post story.")
            print("❌ Failed to post story.", flush=True)
            return
    except Exception as e:
        print(f"❌ Erro em process_story_logic: {e}", flush=True)
        
@app.post("/process/post")
def process_post(data: PostRequest, background_tasks: BackgroundTasks):
    # ✅ Enfileira a função para rodar em background
    background_tasks.add_task(process_post_logic, data.folder_path)
    return {"status": "started", "message": f"Processing {data.folder_path}"}

def process_post_logic(folder_path: str):
    """
    Processes and posts a single image to Instagram:

    Steps:
    1. Checks if `.posted` exists (Skip if already posted).
    2. Reads `caption.txt` if available.
    3. Calls `generate_caption()` with proper inputs.
    4. Uploads the image and posts it to Instagram.
    5. Marks the post as completed using `finalize_post()`.
    """
    try:
        folder = folder_path
        print(f"📂 Checking post folder: {folder}")
        # notify_telegram(f"📂 Checking post folder: {folder}")

        posted_flag = os.path.join(folder, ".posted")
        if os.path.exists(posted_flag):
            return {"message": "✅ Post already completed. Skipping."}

        caption_file = os.path.join(folder, "caption.txt")
        caption_text = ""
        if os.path.exists(caption_file):
            with open(caption_file, "r", encoding="utf-8") as f:
                caption_text = f.read().strip()
            print(f"📜 Loaded caption from {caption_file}")
           # notify_telegram(f"📜 Loaded caption from {caption_file}")

        print("🧐 Generating enhanced caption using AI...",flush=True)
       # notify_telegram("🧐 Generating enhanced caption using AI...")
        inputs = {
            "genero": "Indefinido",
            "caption": caption_text,
            "describe": "Imagem relevante para postagem",
            "estilo": "Divertido, Alegre, descontraído, linguagem simples",
            "pessoa": "Terceira pessoa do singular",
            "sentimento": "Positivo",
            "tamanho": "200 palavras",
            "emojis": "sim",
            "girias": "não"
        }

        image_extensions = ("*.png", "*.jpg", "*.jpeg", "*.webp")
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(folder, ext)))

        if not image_files:
        # raise HTTPException(status_code=404, detail="❌ No image found.")
            print(f"❌ No image found in {folder_path}. Aborting process.", flush=True)
           # notify_telegram(f"❌ No image found in {folder_path}. Aborting process.")
            return  # <-- aqui você simplesmente retorna. Não gera erro HTTP
        try:
            generated_caption = InstagramCaptionCrew().kickoff(inputs)
            print(f"✅ Generated Caption: {generated_caption}",flush=True)
           # notify_telegram(f"✅ Generated Caption: {generated_caption}")
        except:
            print(f"❌ Erro ao gerar caption: {e}", flush=True)
           # notify_telegram(f"❌ Erro ao gerar caption: {e}")           
            return
        
        image_path = image_files[0]
        print(f"📸 Selected image: {image_path}")

        imgur_client = ImageUploader()
        imgurVar = imgur_client.upload_from_path(image_path)
        if not imgurVar:
        # raise HTTPException(status_code=500, detail="❌ Image upload failed.")
            print("❌ Image upload failed.")
           # notify_telegram("❌ Image upload failed.")
            return
        print(f"✅ Uploaded Image URL: {imgurVar['url']}")
       # notify_telegram(f"✅ Uploaded Image URL: {imgurVar['url']}")

        insta_service = InstagramPostService()
        post_id = insta_service.post_image(imgurVar["url"], generated_caption)

        if post_id:
            print(f"✅ Post successful! ID: {post_id}", flush=True)
            notify_telegram(f"✅ Post successful! ID: {post_id}")
            finalize_post(folder, post_id, imgur_client, imgurVar)
            return {"message": "✅ Post successful.", "post_id": post_id}
        else:
            # raise HTTPException(status_code=500, detail="❌ Failed to post to Instagram.")
            print ("❌ Failed to post to Instagram.")
            notify_telegram("❌ Failed to post to Instagram.")
            return

    except Exception as e:
        print(f"❌ Erro em process_post_logic: {e}", flush=True)
        # notify_telegram(f"❌ Erro em process_post_logic: {e}")