from core.ai.describe_image_ollama import OllamaImageDescriber

# Define the image path
image_path = "./assets/20250218_stories_001/1.png"  # Update with your actual image path

# Initialize the LLava image describer
describer = OllamaImageDescriber()

# Get the description
description = describer.describe_image(image_path)

# Print the result
print("🔍 Image Description:")
print(description)
