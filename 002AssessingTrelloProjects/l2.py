# warning control
from crewai import Agent, Task, Crew
import requests
from crewai_tools import BaseTool
import logging
import datetime
import yaml
import json
import os
from config.llm_models import llm_models
from config.helper import load_env
from config.customtools import CardDataFetcherTool, BoardDataFetcherTool, Json2Text
import warnings
warnings.filterwarnings('ignore')
from crewai_tools import JSONSearchTool

# load environment variables
load_env()


# define file path for YAML config
files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}


# Load config from YAML files
configs = {}

for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded config to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']
json_tool = JSONSearchTool()


model1 = "llama32"
model2 = "llama32"

# Creating Agents
data_collection_agent = Agent(
    config=agents_config['data_collection_agent'],
    tools=[BoardDataFetcherTool(), CardDataFetcherTool(), Json2Text()],
    llm=llm_models.get_model(model1)
)

analysis_agent = Agent(
    config=agents_config['analysis_agent'],
    llm=llm_models.get_model(model2)
)

# Creating tasks

data_collection = Task(
    config=tasks_config['data_collection'],
    agent=data_collection_agent
)

data_analysis = Task(
    config=tasks_config['data_analysis'],
    agent=analysis_agent
)

report_generation = Task(
    config=tasks_config['report_generation'],
    agent=analysis_agent,
)

crew = Crew(
    agents=[
        data_collection_agent, analysis_agent
    ],
    tasks=[
        data_collection,
        data_analysis,
        report_generation
    ],

    verbose=True
)
# Executar o CrewAI
logging.info("Running CrewAI...")
start_time=datetime.datetime.now()

result = crew.kickoff()

logging.info("CrewAI Execution Completed.")
end_time = datetime.datetime.now()

logging.info(f"Execution finished at: {end_time}")

elapsed_time = end_time - start_time
elapsed_seconds = int(elapsed_time.total_seconds())
hours, remainder = divmod(elapsed_seconds, 3600)
minutes, seconds = divmod(remainder, 60)

# Format string
elapsed_str = f"{hours}h {minutes}m {seconds}s"

logging.info(f"Elapsed time: {elapsed_str}")

# Verificar e converter `crew.usage_metrics` para um dicionário antes de serializar
usage_metrics_dict = crew.usage_metrics.model_dump() if hasattr(
    crew.usage_metrics, "dict") else {}

# Capturar os modelos usados por cada agente
usage_metrics_str = "\n".join(f"{key}: {value}" for key, value in usage_metrics_dict.items())


# Convert CrewOutput to a dictionary
result_dict = result.model_dump()  # Use .model_dump() if it's a Pydantic model

# Convert JSON to formatted string
json_content = json.dumps(result_dict, indent=4)

task1 = result.tasks_output[0]
task2 = result.tasks_output[1]

# Determinar nome do arquivo de saída
output_base = "execution_output"
output_ext = ".md"
output_file = f"{output_base}{output_ext}"
counter = 1
while os.path.exists(output_file):
    output_file = f"{output_base}_{counter}{output_ext}"
    counter += 1
print(crew.usage_metrics)

# Gerar saída em arquivo Markdown
with open(output_file, "w") as f:
    f.write(f"# CrewAI Execution Report\n\n")
    f.write(f"## Token Usage Metrics\n")
    f.write(f"```\n{usage_metrics_str}\n```\n\n")
    f.write(f"## Models Used per Agent\n")
    f.write(f"```\n{model1}\n```\n\n")
    f.write(f"```\n{model2}\n```\n\n")
    f.write(f"**Start Time:** {start_time}\n\n")
    f.write(f"**End Time:** {end_time}\n\n")
    f.write(f"**Ellapsed Time:** {elapsed_str}\n\n")
    f.write(f"## Project Summary\n")
    f.write(f"{task1}\n\n")
    f.write(f"{task2}\n\n")


