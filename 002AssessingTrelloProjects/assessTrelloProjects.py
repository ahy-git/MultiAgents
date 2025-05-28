import os
import json
import yaml
import logging
import datetime
import warnings
import requests
from crewai import Agent, Task, Crew
from crewai_tools import JSONSearchTool, BaseTool
from config.llm_models import llm_models
from config.helper import load_env
from config.customtools import CardDataFetcherTool, BoardDataFetcherTool, Json2Text

# Suppress warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_env()

# Define file paths for YAML configuration
CONFIG_FILES = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}

# Load configuration from YAML files
configs = {key: yaml.safe_load(open(path, 'r'))
           for key, path in CONFIG_FILES.items()}

# Extract agent and task configurations
agents_config, tasks_config = configs['agents'], configs['tasks']

# Define models
MODEL_1, MODEL_2 = "gpt4omini", "llama32"

# Initialize tools
json_tool = JSONSearchTool()
board_fetch_tool = BoardDataFetcherTool()
card_fetch_tool = CardDataFetcherTool()
json2text_tool = Json2Text()

# Create Agents
data_collection_agent = Agent(
    config=agents_config['data_collection_agent'],
    tools=[board_fetch_tool,card_fetch_tool],
    llm=llm_models.get_model(MODEL_1)
)

analysis_agent = Agent(
    config=agents_config['analysis_agent'],
    llm=llm_models.get_model(MODEL_2)
)

hallucination_check_agent = Agent (
    config=agents_config['hallucination_check_agent'],
    llm=llm_models.get_model(MODEL_2)
)
# Create Tasks
data_collection = Task(
    config=tasks_config['data_collection'], agent=data_collection_agent)
data_analysis = Task(
    config=tasks_config['data_analysis'], agent=analysis_agent)
report_generation = Task(
    config=tasks_config['report_generation'], agent=analysis_agent)
hallucination_check = Task (
    config=tasks_config['hallucination_check'], agent=hallucination_check_agent
)

# Initialize Crew
crew = Crew(
    agents=[data_collection_agent, analysis_agent],
    tasks=[data_collection, data_analysis, report_generation],
    verbose=True
)

# Execute CrewAI
logging.info("Running CrewAI...")
start_time = datetime.datetime.now()
result = crew.kickoff()
end_time = datetime.datetime.now()
logging.info("CrewAI Execution Completed.")
logging.info(f"Execution finished at: {end_time}")

# Calculate elapsed time
elapsed_seconds = int((end_time - start_time).total_seconds())
hours, remainder = divmod(elapsed_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
elapsed_str = f"{hours}h {minutes}m {seconds}s"
logging.info(f"Elapsed time: {elapsed_str}")

# Handle usage metrics
usage_metrics_dict = crew.usage_metrics.model_dump(
) if hasattr(crew.usage_metrics, "dict") else {}
usage_metrics_str = "\n".join(
    f"{key}: {value}" for key, value in usage_metrics_dict.items())

# Convert CrewOutput to a formatted JSON string
json_content = json.dumps(result.model_dump(), indent=4)

# Extract task outputs
task_outputs = "\n\n".join(str(task) for task in result.tasks_output)

# Determine output file name
output_base, output_ext = "execution_output", ".md"
counter, output_file = 1, f"{output_base}{output_ext}"
while os.path.exists(output_file):
    output_file = f"{output_base}_{counter}{output_ext}"
    counter += 1

# Write execution report to Markdown file
with open(output_file, "w") as f:
    f.write(f"# CrewAI Execution Report\n\n")
    f.write(f"## Token Usage Metrics\n```{usage_metrics_str}\n```\n\n")
    f.write(
        f"## Models Used per Agent\n```{MODEL_1}\n```\n\n```{MODEL_2}\n```\n\n")
    f.write(f"**Start Time:** {start_time}\n\n")
    f.write(f"**End Time:** {end_time}\n\n")
    f.write(f"**Elapsed Time:** {elapsed_str}\n\n")
    f.write(f"## Project Assessment\n{task_outputs}\n\n")

print(crew.usage_metrics)
