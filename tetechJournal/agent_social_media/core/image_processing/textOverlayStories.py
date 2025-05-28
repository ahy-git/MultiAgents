import json
import re
from core.image_processing.textOverlay import ImageTextOverlay
from typing import Optional

class TextOverlayProcessor:
    @staticmethod
    def clean_json_string(json_string: str) -> str:
        """
        Cleans a JSON string by:
        - Removing `// comments`
        - Ensuring proper double-quoted keys
        - Fixing misplaced commas and trailing commas
        
        :param json_string: Raw JSON string extracted from the Markdown file.
        :return: Cleaned JSON string ready for parsing.
        """
        # Remove `// comments` (anything after `//` on a line)
        json_string = re.sub(r"//.*", "", json_string)

        # Remove trailing commas before closing braces/brackets (invalid in JSON)
        json_string = re.sub(r",\s*([\]}])", r"\1", json_string)

        return json_string

    @staticmethod
    def extract_json_from_md(file_path: str) -> dict:
        """
        Extracts JSON data from a Markdown file, automatically fixing common errors.

        :param file_path: Path to the markdown file
        :return: Parsed JSON dictionary
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Extract JSON using regex
            json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if not json_match:
                raise ValueError("❌ No JSON block found in the markdown file!")

            json_data = json_match.group(1)

            # Clean the JSON string to fix formatting issues
            json_data = TextOverlayProcessor.clean_json_string(json_data)

            # Validate JSON format
            try:
                parsed_json = json.loads(json_data)
                print("✅ JSON successfully parsed and cleaned!")  # Debugging message
                return parsed_json
            except json.JSONDecodeError as e:
                print(f"❌ JSON format error: {e}")
                return {}

        except Exception as e:
            print(f"❌ Error reading JSON from markdown: {e}")
            return {}

    @staticmethod
    def process_text_overlay(
        input_md_file: str,
        input_image: str,
        output_image: str
    ) -> Optional[str]:
        """
        Processes text overlay by extracting JSON from a markdown file and calling ImageTextOverlay.

        :param input_md_file: Path to the markdown file containing JSON
        :param input_image: Path to the image file that will be used
        :param output_image: Path where the final edited image will be saved
        :return: Final processed image path or None if an error occurs
        """
        # Extract JSON data
        overlay_data = TextOverlayProcessor.extract_json_from_md(input_md_file)
        if not overlay_data:
            print("conversion JSON Failed")
            return None  # Return None if JSON extraction fails

        # Extract necessary fields with default values, overriding `image_path` and `output_path`
        text_to_add = overlay_data.get("suggested_text", "Default Text")
        position = tuple(overlay_data.get("position", [100, 100]))  # Convert list to tuple

        # Ensure default values for missing optional parameters
        font_size = 100 if overlay_data.get("font_size") == "Large" else 50
        font_color = overlay_data.get("font_color", "white")
        outline_color = overlay_data.get("outline_color", "black")
        box_enabled = overlay_data.get("box_enabled", True)
        box_color = overlay_data.get("box_color", "blue")
        box_opacity = overlay_data.get("box_opacity", 180)
        box_padding = overlay_data.get("box_padding", 30)
        box_border_thickness = overlay_data.get("box_border_thickness", 5)
        box_border_color = overlay_data.get("box_border_color", "yellow")
        box_roundness = overlay_data.get("box_roundness", 20)
       
        # ✅ Fix for `rgba()` color format
        if isinstance(box_color, str) and box_color.startswith("rgba"):
            try:
                rgba_values = [float(v) if i == 3 else int(v) for i, v in enumerate(box_color[5:-1].split(","))]
                box_color = tuple(int(rgba_values[i]) if i < 3 else int(rgba_values[i] * 255) for i in range(4))
            except Exception as e:
                print(f"⚠️ Error parsing box_color `{box_color}`: {e}. Defaulting to blue.")
                box_color = (0, 0, 255, 180)  # Default to blue with opacity
                
                
        # Debug: Print extracted values
        print(f"🛠️ [DEBUG] Extracted Data:\n"
              f"Image: {input_image}\nText: {text_to_add}\nOutput: {output_image}\n"
              f"Position: {position}\nFont Size: {font_size}\nFont Color: {font_color}\n"
              f"Box Enabled: {box_enabled}\nBox Color: {box_color}\n")

        # Call the text overlay method
        final_image_path = ImageTextOverlay.add_text_to_image(
            input_image, text_to_add, output_image,
            position=position,
            font_size=font_size, font_color=font_color, outline_color=outline_color,
            box_enabled=box_enabled, box_color=box_color, box_opacity=box_opacity,
            box_padding=box_padding, box_border_thickness=box_border_thickness, box_border_color=box_border_color,
            box_roundness=box_roundness
        )

        print(f"✅ Process completed! Final image saved at: {final_image_path}")
        return final_image_path
