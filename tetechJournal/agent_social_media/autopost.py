import os
import glob
from core.ai.story_generation_crew import StoryGenerationCrew
from core.image_processing.ResizeImageStories import EditImageStories
from core.image_processing.textOverlayStories import TextOverlayProcessor
from core.social_media.instagram_post import InstagramPostService
from infra.tasks.postFinalize import finalize_post
from infra.tasks.pendingPosts import get_pending_posts
from infra.imgur.imgur_service import ImageUploader
from PIL import Image
from core.ai.generate_caption import InstagramCaptionCrew

def post_story(post_folder):
    """
    Automates the full Instagram Story posting process:
    - Checks for `.posted` to avoid reposts.
    - Generates text if `InputsImage.md` does not exist.
    - Resizes image to Instagram Stories format.
    - Adds text overlays, ensuring no overflow.
    - Uploads, posts, and cleans up images.
    """

    print(f"📂 Checking post folder: {post_folder}")

    # Step 1️⃣: **Check if `.posted` exists (Avoid Reposting)**
    posted_flag = os.path.join(post_folder, ".posted")
    if os.path.exists(posted_flag):
        print(f"✅ Story already posted. Skipping: {posted_flag}")
        return

    # Step 1.1️⃣: **Check if `InputsImage.md` already exists**
    input_md = os.path.join(post_folder, "InputsImage.md")
    goto_step5 = os.path.exists(input_md)

    # Step 2️⃣: **Find any image in the folder**
    image_extensions = ("*.png", "*.jpg", "*.jpeg", "*.webp")
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(post_folder, ext)))

    if not image_files:
        print(f"❌ No image found in {post_folder}. Aborting process.")
        return

    # Use the first image found
    input_image_path = image_files[0]
    print(f"✅ Found image: {input_image_path}")

    # Step 4️⃣: Find the first `_rszd` image before skipping
    rszd_images = glob.glob(os.path.join(post_folder, "*_rszd.*"))
    
    resized_image_path = rszd_images[0] if rszd_images else os.path.join(
    post_folder, f"{os.path.splitext(os.path.basename(input_image_path))[0]}_rszd.png"
    )
    
    if not goto_step5:
        # Step 3️⃣: **Run CrewAI Story Generation**
        print("🚀 Running Story Generation CrewAI Pipeline...")

        width,height = Image.open(input_image_path).size
        caption_humano = open(glob.glob("*.txt")[0], encoding="utf-8").read().strip() if glob.glob("*.txt") else ""

        crew = StoryGenerationCrew(image_path=input_image_path, output_path=input_md)
        final_output = crew.kickoff(image_folder=post_folder, image_path=input_image_path, caption_text = caption_humano,img_width=width,img_height=height)

        if not final_output:
            print("❌ Story Generation Failed. Aborting process.")
            return

        print(f"✅ Story Generation Completed. Data saved at: {final_output}")

        # Step 4️⃣: **Resize Image for Instagram Stories**
        print(f"🚀 Resizing image for Instagram Stories format...")
        final_image = EditImageStories.transform_to_story_format(input_image_path, resized_image_path)

        if not final_image:
            print("❌ Failed to resize image. Aborting process.")
            return

        print(f"✅ Image Resized: {final_image}")

    # Step 5️⃣: **Ensure `resized_image_path` exists before processing text overlay**
    if not os.path.exists(resized_image_path):
        print(f"⚠️ Warning: Resized image not found. Using original image instead.")
        resized_image_path = input_image_path  # Fallback to the original image

    # Step 5️⃣: **Apply Text Overlay to Story**
    processed_image_path = os.path.join(post_folder, "processed_image.png")
    print("🖋️ Adding text overlay to the image...")

    final_story_image = TextOverlayProcessor.process_text_overlay(input_md, resized_image_path, processed_image_path)
    if not final_story_image:
        print("❌ Failed to process text overlay. Aborting process.")
        return

    print(f"✅ Final Story Image Ready: {final_story_image}")

    # Step 6️⃣: **Upload and Post the Final Story Image**
    imgur_client = ImageUploader()
    imgurVar = imgur_client.upload_from_path(final_story_image)

    if not imgurVar:
        print("❌ Image upload failed.")
        return

    print(f"✅ Uploaded Image: {imgurVar['url']}")

    insta_service = InstagramPostService()
    story_id = insta_service.post_story(imgurVar["url"])

    if story_id:
        print(f"✅ Story successfully posted! ID: {story_id}")
        finalize_post(post_folder, story_id, imgur_client, imgurVar)

def post_carousel(folder):
    return
def post_reel(folder):
    return
def post_standard(folder):
    """
    Processes and posts a single image to Instagram.

    Steps:
    1. Checks if `.posted` exists (Skip if already posted).
    2. Reads `caption.txt` if available.
    3. Calls `generate_caption()` with proper inputs.
    4. Uploads the image and posts it to Instagram.
    5. Marks the post as completed using `finalize_post()`.

    :param folder: Directory containing the post's content.
    """

    print(f"📂 Checking post folder: {folder}")

    # Step 1️⃣: Check if `.posted` exists
    posted_flag = os.path.join(folder, ".posted")
    if os.path.exists(posted_flag):
        print(f"✅ Post already completed. Skipping: {posted_flag}")
        return

    # Step 2️⃣: Read caption from `caption.txt`, if available
    caption_file = os.path.join(folder, "caption.txt")
    caption_text = ""
    if os.path.exists(caption_file):
        with open(caption_file, "r", encoding="utf-8") as f:
            caption_text = f.read().strip()
        print(f"📝 Loaded caption from {caption_file}")

    # Step 3️⃣: Generate AI-enhanced caption
    print("🤖 Generating enhanced caption using AI...")
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
    
    # Step 4️⃣: Find an image in the folder
    image_extensions = ("*.png", "*.jpg", "*.jpeg", "*.webp")
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder, ext)))
    if not image_files:
        print(f"❌ No image found in {folder}. Aborting process.")
        return

    generated_caption = InstagramCaptionCrew().kickoff(inputs)
    print(f"✅ Generated Caption: {generated_caption}")

    image_path = image_files[0]  # Use the first image found
    print(f"📸 Selected image: {image_path}")

    # Step 5️⃣: Upload the image to Imgur
    imgur_client = ImageUploader()
    imgurVar = imgur_client.upload_from_path(image_path)

    if not imgurVar:
        print("❌ Image upload failed. Aborting.")
        return

    print(f"✅ Uploaded Image URL: {imgurVar['url']}")

    # Step 6️⃣: Post to Instagram
    insta_service = InstagramPostService()
    post_id = insta_service.post_image(imgurVar["url"], generated_caption)

    if post_id:
        print(f"✅ Post successful! ID: {post_id}")
        finalize_post(folder, post_id, imgur_client, imgurVar)
    else:
        print("❌ Failed to post to Instagram.")

def main():
    """
    Main function to process and post all pending stories.
    """
    print("🔍 Checking for pending Instagram Stories...")

    story_folders = get_pending_posts("stories")
    if story_folders:
        for story in story_folders:
            post_story(story)

    carousel_folders = get_pending_posts("carousels")
    if carousel_folders:
        for carousel in carousel_folders:
            post_carousel(carousel)

    reels_folders = get_pending_posts("reels")
    if reels_folders:
        for reel in reels_folders:
            post_reel(reel)

    post_folders = get_pending_posts("posts")
    if post_folders:
        for post in post_folders:
            post_standard(post)

    print("✅ All stories processed!")


if __name__ == "__main__":
    main()
