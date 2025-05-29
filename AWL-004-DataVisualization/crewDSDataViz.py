import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from MyLLM import MyLLM
from toolCodeInterpreter import CodeInterpreterTool

load_dotenv()

class DataAnalysisCrew:
    def __init__(self):
        self.llm = MyLLM.Ollama_qwen3
        self.e2b_api_key = os.getenv("E2B_API_KEY")
        self.output_dir = "output_visualizations"
        self.code_tool = CodeInterpreterTool(self.e2b_api_key, self.output_dir)
        self.crew = self._setup_crew()
        self.current_dataset_path = None  # To store the current dataset path

    def _setup_crew(self):
        analyst = Agent(
            role="Senior Data Analyst",
            goal=(
                "Analyze datasets to uncover insights and create visualizations "
                "that answer business questions"
            ),
            backstory=(
                "Expert in statistical analysis and data visualization with "
                "10+ years experience in transforming raw data into actionable insights. "
                "Always uses '/dataset.csv' as the file path when loading data."
            ),
            tools=[self.code_tool],
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description=(
                "Analyze the dataset to address: {query}\n"
                "IMPORTANT: The dataset has been uploaded to the sandbox and is always available at '/dataset.csv'.\n"
                "Follow these steps:\n"
                "1. Load the data using: `pd.read_csv('/dataset.csv')`\n"
                "2. Preprocess the data if needed\n"
                "3. Conduct exploratory analysis\n"
                "4. Create appropriate visualizations\n"
                "5. Summarize key findings\n\n"
                "Use the CodeInterpreterTool for all code execution."
            ),
            expected_output=(
                "Comprehensive analysis report including:\n"
                "- Data summary statistics\n"
                "- Key insights from analysis\n"
                "- Visualization file paths\n"
                "- Interpretation of results"
            ),
            agent=analyst
        )

        return Crew(
            agents=[analyst],
            tasks=[task],
            process=Process.sequential
        )

    def kickoff(self, dataset_path: str, query: str) -> dict:
        try:
            # Store current dataset path for tool access
            self.code_tool._current_dataset_path = dataset_path
            
            # Run the crew with only the query
            results = self.crew.kickoff(inputs={"query": query})
            
            return {
                "analysis_report": results,
                "visualizations": self.code_tool.generated_images
            }
        finally:
            self.code_tool.close()

if __name__ == "__main__":
    # Test configuration
    test_dataset = "sample.csv"
    test_query = "Make a comparison of salaries between departments"
    
    # Create sample dataset if it doesn't exist
    if not os.path.exists(test_dataset):
        with open(test_dataset, "w") as f:
            f.write("Name,Department,Salary\nJohn,Engineering,100000\nJane,Marketing,95000\nBob,Engineering,110000\nAlice,Marketing,90000")
    
    crew = DataAnalysisCrew()
    
    # Explain the process
    print(f"🔍 Starting analysis with dataset: {test_dataset}")
    print(f"📝 Query: {test_query}")
    print("💾 Dataset will be uploaded to sandbox as '/dataset.csv'")
    print("🚀 Agent will access it using pd.read_csv('/dataset.csv')")
    
    result = crew.kickoff(test_dataset, test_query)
    
    print("\n📊 Analysis Report:")
    print(result["analysis_report"])
    
    print("\n🖼️ Generated Visualizations:")
    for viz in result["visualizations"]:
        print(f"- {viz}")