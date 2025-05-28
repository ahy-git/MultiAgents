import os
from core.image_processing.ResizeImageStories import EditImageStories

# Define input and output image paths
input_image_path = os.path.abspath(
    "./assets/20250218_stories_001/1.png").replace("\\", "/")
output_image_path = os.path.abspath(
    "./assets/20250218_stories_001/1_rszd.png").replace("\\", "/")

# Debug: Print the absolute path
print(f"🔍 Checking Image Path: {input_image_path}")

# Ensure the file still exists after formatting the path
if not os.path.exists(input_image_path):
    print(f"❌ File not found after path formatting: {input_image_path}")
else:
    print(f"✅ Input image exists: {input_image_path}")

# Run the resize function
print(f"🚀 Resizing image for Instagram Stories format...")
final_image = EditImageStories.transform_to_story_format(
    input_image_path, output_image_path)

if final_image:
    print(f"🎉 Final processed image saved at: {final_image}")
else:
    print("❌ Failed to resize the image.")
