# GEMINI WORKS FOR SIMPLE TASKS!

# Warning control
from crewai_tools import JSONSearchTool
import os
from typing import Dict, Optional, List, Set, Tuple
from pydantic import BaseModel, Field, ConfigDict
from crewai import Agent, Task, Crew
import yaml
from config.helper import load_env
from config.llm_models import llm_models
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_env()

# model = "gpt4omini"
model = 'geminiflash2'
# Define file paths for YAML configurations
files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml',
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

jsonRagTool = JSONSearchTool(json_path='./resultado_importacao.json')


# Creating Agents
jsonrag_agent = Agent(
    config=agents_config['json_agent'],
    tools=[jsonRagTool],
    llm=llm_models.get_model(model)
)


# Creating Tasks
jsonrag_task = Task(
    config=tasks_config['jsonRAG_task'],
    agent=jsonrag_agent,
    output_file='ncm1.md'
)

# Creating Crew
jsonRAGCrew = Crew(
    agents=[
        jsonrag_agent
    ],
    tasks=[
        jsonrag_task,
    ],
    verbose=True
)

ncm = input("digite o ncm ou descricao:")
print(ncm)
inputs = {"input_ncm": ncm}
result = jsonRAGCrew.kickoff(inputs=inputs)

print(result)
