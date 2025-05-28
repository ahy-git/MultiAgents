from core.image_processing.textOverlayStories import TextOverlayProcessor

input_md = "./assets/20250218_stories_001/inputsImage.md"
input_image_path = "./assets/20250218_stories_001/1_rszd.png"
output_image_path = "./assets/20250218_stories_001/processed_image.png"

final_image = TextOverlayProcessor.process_text_overlay(input_md, input_image_path, output_image_path)

if final_image:
    print(f"🎉 Final processed image saved at: {final_image}")
else:
    print("❌ Failed to process text overlay.")
