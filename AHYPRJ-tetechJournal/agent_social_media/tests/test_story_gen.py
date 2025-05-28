import os
from core.ai.story_generation_crew import StoryGenerationCrew

# Define the test folder and image path
TEST_FOLDER = "./assets/20250218_stories_001"

# Find the first image in the test folder
def find_image(folder):
    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            return os.path.join(folder, file)
    return None

# Get the test image path
test_image = find_image(TEST_FOLDER)

if not test_image:
    print("❌ No image found in the test folder. Please add an image.")
    exit()

# Define output path
output_image = os.path.join(TEST_FOLDER, "edited_story.png")

# Run the CrewAI Story Generation Pipeline
print("🚀 Running Story Generation CrewAI Test...")
crew = StoryGenerationCrew(image_path=test_image, output_path=output_image)
final_output = crew.kickoff(image_folder=TEST_FOLDER, image_path=test_image)

if final_output:
    print(f"✅ Test completed successfully! Final story saved at: {final_output}")
else:
    print("❌ Test failed. Please check logs for errors.")
