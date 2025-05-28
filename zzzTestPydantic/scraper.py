# GEMINI WORKS FOR SIMPLE TASKS!

# Warning control
import warnings
warnings.filterwarnings('ignore')

from config.llm_models import llm_models

# Load environment variables
from config.helper import load_env
load_env()

import os
import yaml
from crewai import Agent, Task, Crew
import litellm
# litellm._turn_on_debug()

model = "geminiflash"
model2 = 'geminiflash'
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

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional, List, Set, Tuple

    
class Topics(BaseModel):
    topic: str = Field (...,description="Topic Name if found")
    definitions: str = Field (...,description="definition found in topic")
    PositiveConcepts: str = Field (...,description="positive facts found in topic")
    NegativeConcepts: str = Field (...,description="negative found in topic")
    links: List[str] = Field (..., description="Links found in topic")
    challenges: str = Field (...,description="challenges found in topic")
    summaryTopic: str = Field (...,description="summary of the topic")

class Content(BaseModel):
    name: str = Field(..., description="title of the webpage")
    summary: str = Field(..., description="summary of the text")
    challenges: str = Field(..., description="most difficult challenges found by the author in the text")
    Topics: str = List[Topics]    

from crewai_tools import SerperDevTool, ScrapeWebsiteTool
# Creating Agents
scraper_agent = Agent(
  config=agents_config['scraper_agent'],
  tools=[ScrapeWebsiteTool()],
  llm=llm_models.get_model(model)
)

organizer_agent = Agent(
  config=agents_config['organizer_agent'],
  llm=llm_models.get_model(model)
)

# Creating Tasks
scrape_task = Task(
  config=tasks_config['scrape'],
  agent=scraper_agent,
)

organize_task = Task(
  config=tasks_config['organize'],
  agent=organizer_agent,
  context=[scrape_task],
  output_pydantic=Content,
)

# Creating Crew
PydanticTest = Crew(
  agents=[
    scraper_agent,
    organizer_agent,
  ],
  tasks=[
    scrape_task,
    organize_task,
  ],
  verbose=True
)

url={'url':'https://dev.to/myogeshchavan97/top-10-react-librariesframeworks-for-2025-50i4'}
result = PydanticTest.kickoff(inputs=url)

print(result.dict())  # Pydantic v1
print(result.model_dump())  # Pydantic v2
