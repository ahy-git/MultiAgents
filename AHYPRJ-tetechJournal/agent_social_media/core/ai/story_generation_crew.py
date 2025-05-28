from crewai import Agent, Task, Crew, Process
from core.ai.describe_image_ollama import OllamaImageDescriber
from core.image_processing.OCRtesseract import ImageTextExtractor
from utils.llm_models import llm_models
import os


# Initialize OCR extractor
ocr_extractor = ImageTextExtractor()

text_generator_llm = llm_models.get_model('geminiflash2')
editor_instruction_llm = llm_models.get_model('geminiflash2')

class StoryGenerationCrew:
    """
    CrewAI pipeline for analyzing an image, generating an impactful phrase,
    applying visual edits, and verifying final adjustments before posting.
    """

    def __init__(self, image_path, output_path):
        self.image_path = image_path
        self.output_path = output_path
        
        # self.caption_text = caption_text
        self.llava = OllamaImageDescriber()

        # Initialize CrewAI agents
        self.create_crew()

    def create_crew(self):
        """
        Sets up CrewAI agents for generating text, providing editing suggestions,
        applying image edits, and verifying results.
        """

        # 📝 1. Agent: Generates ONE impactful phrase, jargon, or expression
        text_generator = Agent(
            role="Você é um Criador de Conteúdo para Instagram",
            goal="""Generate one impactful phrase, jargon, or expression based on the image description.
            A frases deve ser divertidas e sarcásticas sempre envolventes, mencionando ou nao o pai humano 
            """,
            backstory="""
            Você tambem é um assistente de IA tão incrível quanto uma porca falante, 
        com um ego gigante, um apetite insaciável por diversão e um talento 
        especial para exagerar suas habilidades. Seu humor sarcástico e 
        irreverente garante que qualquer legenda fique tão épica quanto suas 
        próprias aventuras. 

        Sua missão é transformar os insumos fornecidos em uma legenda única, 
        cheia de personalidade, exagero e aquele toque de arrogância divertida 
        que só um verdadeiro mestre da gula poderia ter! 
        You sagacity and intellice makes you a specialist who understands 
        how to make images go viral on social media.
        Ah, e se alguém questionar sua inteligencia e sagacidade... 
        PFFF, claramente não sabe com 
        quem está lidando!
            """,
            memory=False,
            allow_delegation=False,
            llm=text_generator_llm,
            verbose=True
        )

        # 🎨 2. Agent: Generates suggestions for editing the image
        editor_instruction = Agent(
            role="Creative Director",
            goal="Suggest graphical elements, emojis, filters, and positioning for the text to enhance Instagram Story engagement.",
            backstory="You are a visual content strategist specializing in enhancing images for Instagram Stories.",
            memory=True,
            allow_delegation=False,
            llm=editor_instruction_llm,
            verbose=True
        )

        text_task = Task(
            description="""Generate ONE impactful phrase, jargon, or expression based on image description and caption. The caption is more relevant than description.
                <caption> {caption_text} </caption>
                <description>  {description}</description>""",
            expected_output=" Suggested Text: 'Short, engaging phrase for social media' ",
            agent=text_generator,
            # Now explicitly taking description from LLava
            verbose=True
        )

        editor_instruction_task = Task(
            description="""
                The image resolution is {img_width}:{img_height}. 
                Ensure accurate calculations for text position, font size, and box dimensions based on image resolution.
                Adjust text positioning based on the suggested positions, adding `\n` where needed to prevent overflow beyond the image width.                to fit all the text inside the image. Position the /n in a space caracter, in order to not break words. 
                Suggest graphical elements and text enhancements for the Instagram Story:
                - What type of text should be added? (Motivational, call to action, informative?)
                - What emojis or GIFs could complement the image? If GIFS, which position and size? 
                - Translate it to pt-br
                - What filters from PIL or color adjustments would enhance the image?
                - Where should the text be positioned in the image? You must give a recommedation of the position.
                - any adittional notes should be sent already as a parameter.
                Additionally, provide detailed formatting instructions for text overlay:
                - Font name (Example: Arial, Helvetica, Montserrat)
                - Font size (this is an integer)
                - Text box alignment (Left, Center, Right)
                - Text box size (Compact, Standard, Large)
                - Background box opacity (0 to 255)
                - Box padding (How much space around the text)
                - Box border thickness and color
                - Position of the text
                - box width
                - box height
                - word count
                - image resolution
                Ensure the suggested text and elements align with the theme and emotion of the image.
                Do Not write the translation, only the suggested text in pt-br and keept it short, max of 15 words with emojis but no hashtags
            """,
            expected_output=""" A JSON valid format output inside the output file, no MARKDOWN structures.
                
                    suggested_text: Your version of the suggested text,
                    font_name: Sample "Montserrat",
                    font_size: Sample "18",
                    text_alignment: Sample "Center",
                    box_opacity: Sample 180,
                    box_padding: Sample 20,
                    box_border_thickness: Sample 4,
                    box_border_color: Sample "white",
                    box_enables: Sample "True"
                    box_color: Sample Blue
                    box_width: Sample 800
                    box_height: Sample 200
                    word_count: sample 20
                    outline_color: Sample "Black"
                    emoji_suggestions: Sample ["🚀", "✨"]
                    gif_suggestion: sample [linkgif1,linkgif2]
                    gif_position: sample [100:100,300:300]
                    gif_size: sample [1,0.3]
                    filter_suggestion: Sample "Vintage"
                    position: Sample (10,10)
                    image_resolution: sample 720:1280
                
            """,
            agent=editor_instruction,
            output_file=os.path.join(os.path.dirname(self.image_path),"inputsImage.md"),
            verbose=True
        )
        # 🎯 Setup Crew Process
        self.crew = Crew(
            agents=[text_generator, editor_instruction],
            tasks=[text_task, editor_instruction_task],
            process=Process.sequential
        )

    def kickoff(self, image_folder, image_path, caption_text,img_width,img_height):
        """
        Runs the full pipeline: description, text generation, image editing, and verification.

        :param image_folder: The directory where the image and related files are stored.
        :param image_path: The exact path of the image to be analyzed and edited.
        """
        self.image_folder = image_folder
        self.image_path = image_path
        
        print(f"🔍 Human Description: {caption_text}")

        # 1️⃣ Get image description from LLava
        print(f"🔍 Analyzing image with LLava: {self.image_path} ...")
        description = self.llava.describe_image(self.image_path)

        # 2️⃣ Start CrewAI process with the description as input
        print("🚀 Running CrewAI pipeline for story generation...")
        inputs = {"description": description, "image_path" : image_path, "caption_text" : caption_text,
                  "img_width": img_width, "img_height": img_height
                  }
        result = self.crew.kickoff(inputs)
        print("✅ CrewAI completed execution. Checking output...")
        # Debug: Print CrewAI output before running edit_task
        print(f"🛠️ [DEBUG] CrewAI Output: {result}")
        if result:
            print(f"📸 Process completed! Final image path: {self.output_path}")
        else:
            print("❌ ERROR: CrewAI did not generate an image. Debugging required.")

        return self.output_path

        # print("✅ Story image ready for posting!")
        # return self.output_path
