## GPT4o mini has no vision

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM
from toolDuckDuckgo import DuckDuckGoTool
from crewai_tools import VisionTool

load_dotenv()

class MedicalImageDiagnosisCrew:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.llm = MyLLM.geminiflash20
        self.search_tool = DuckDuckGoTool()
        self.vision_tool = VisionTool(image_path_url=self.image_path)  # pass LLM to the VisionTool
        self.crew = self._setup_crew()

    def _setup_crew(self):
        # Agent
        radiologist = Agent(
            role="Medical Imaging Expert",
            goal="Diagnose medical images and provide comprehensive AI-powered analysis",
            backstory=(
                "You are a top-tier radiologist AI with deep understanding of diagnostic imaging, "
                "responsible for evaluating image modality, key findings, diagnosis, lay explanation, "
                "and recent medical research using DuckDuckGo."
            ),
            tools=[self.search_tool, self.vision_tool],
            llm=self.llm,
            verbose=True
        )

        # Task
        analysis_task = Task(
            description=(
                "Use the VisionTool to analyze the medical image at `{image_path}`.\n\n"
                "### 1. Image Type & Region\n"
                "- Specify modality (e.g., X-ray, MRI, CT)\n"
                "- Identify anatomical region\n"
                "- Comment on technical quality\n\n"
                "### 2. Key Findings\n"
                "- Describe abnormalities with location, size, shape, severity\n"
                "- Include measurements if applicable\n\n"
                "### 3. Diagnostic Assessment\n"
                "- Primary diagnosis with confidence\n"
                "- Differential diagnoses\n"
                "- Urgent findings\n\n"
                "### 4. Patient-Friendly Explanation\n"
                "- Simplified language without jargon\n"
                "- Use analogies if needed\n\n"
                "### 5. Research Context\n"
                "- Use DuckDuckGo to find similar case studies and treatments\n"
                "- Provide 2-3 useful links or sources"
            ),
            expected_output="Detailed AI diagnosis report with markdown formatting.",
            agent=radiologist,
        )

        return Crew(
            agents=[radiologist],
            tasks=[analysis_task],
            process=Process.sequential
        )

    def kickoff(self) -> str:
        result = self.crew.kickoff(inputs={
            "image_path": self.image_path
        })
        return result


if __name__ == "__main__":
    # Test run
    test_image_path = "example_xray.jpg"
    print(f"🖼️ Uploading image: {test_image_path}")

    if not os.path.exists(test_image_path):
        raise FileNotFoundError("You must provide an example_xray.jpg to run this test.")

    crew = MedicalImageDiagnosisCrew(image_path=test_image_path)
    result = crew.kickoff()
    print("\n📋 Final Medical Diagnosis Report:\n")
    print(result.raw if hasattr(result, "raw") else result)
