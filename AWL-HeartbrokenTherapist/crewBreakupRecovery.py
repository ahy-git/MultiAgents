from crewai import Agent, Task, Crew, Process
from toolDuckDuckgo import DuckDuckGoTool
from MyLLM import MyLLM

class BreakupRecoveryCrew:
    def __init__(self):
        self.llm = MyLLM.geminiflash15
        self.duckducktool = DuckDuckGoTool()
        self.crew = self._setup_crew()
        self.tasks = []

    def _setup_crew(self) -> Crew:
        # Define Agents
        therapist = Agent(
            role="Empathetic Therapist",
            goal="Provide compassionate emotional support to someone going through a breakup",
            backstory="You listen with empathy, validate feelings, and share comforting words and relatable experiences.",
            llm=self.llm,
            verbose=True
        )

        closure = Agent(
            role="Closure Message Creator",
            goal="Help the user express unsent feelings and achieve emotional closure",
            backstory="You specialize in writing heartfelt closure messages and designing emotional release exercises.",
            llm=self.llm,
            verbose=True
        )

        planner = Agent(
            role="Recovery Routine Planner",
            goal="Design a practical 7-day recovery plan with self-care activities and empowering routines",
            backstory="You focus on supporting post-breakup recovery with actionable daily challenges and positive habits.",
            llm=self.llm,
            verbose=True
        )

        brutal = Agent(
            role="Brutally Honest Advisor",
            goal="Provide raw and constructive feedback with objectivity and clarity",
            backstory="You offer no-nonsense insights to help the user understand the breakup and move forward, using factual reasoning and DuckDuckGo search.",
            tools=[self.duckducktool],
            llm=self.llm,
            verbose=True
        )

        # Define Tasks
        t1 = Task(
            name="Emotional Support",
            description="Analyze user's feelings and optional images. Respond with comforting support and empathy.",
            expected_output="A natural-language message with validation, comfort, and support.",
            agent=therapist
        )

        t2 = Task(
            name="Closure Content",
            description="Generate emotional closure content: templates for unsent messages, emotional release rituals, and forward-focused suggestions.",
            expected_output="Formatted closure content with multiple emotional support formats.",
            agent=closure
        )

        t3 = Task(
            name="7-day Recovery Plan",
            description="Create a 7-day breakup recovery plan with self-care, digital detox, challenges, and playlist suggestions.",
            expected_output="A daily plan with tasks, motivation, and lifestyle structure.",
            agent=planner
        )

        t4 = Task(
            name="Brutal feedback",
            description="Provide direct, factual analysis of the situation. Include growth advice and clear action points.",
            expected_output="Raw perspective and actionable insights, avoiding sugar-coating.",
            agent=brutal
        )

        self.tasks = [t1,t2,t3,t4]

        return Crew(
            agents=[therapist, closure, planner, brutal],
            tasks=[t1, t2, t3, t4],
            process=Process.sequential)

    def kickoff(self, user_input: str, images: list = None) -> list:
        return self.crew.kickoff(inputs={"user_input": user_input, "images": images or []})


if __name__ == "__main__":
    user_input = (
        "We were together for 3 years. It ended abruptly after I found out they had been emotionally distant for months. "
        "I feel confused, sad, and a bit angry. I just want to understand what happened and how to move forward."
    )

    images = []

    crew_instance = BreakupRecoveryCrew()
    result = crew_instance.kickoff(user_input=user_input, images=images)

    print("\n✅ Crew execution finished.\n")

for i, task_result in enumerate(result.tasks_output, 1):
    print(f"\n🧠 Task {i}")
    print(f"📄 Description: {task_result.description}")
    print(f"📌 Summary: {task_result.summary}")
    print(f"📝 Raw Output:\n{task_result.raw}")

    if task_result.json_dict:
        print(f"📦 JSON Output:\n{task_result.json_dict}")

    if task_result.pydantic:
        print(f"✅ Pydantic Output:\n{task_result.pydantic}")

