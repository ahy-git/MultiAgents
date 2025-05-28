# GEMINI WORKS FOR SIMPLE TASKS!

# Warning control
from crewai_tools import GithubSearchTool
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
GHKEY = os.getenv("GHAGENTKEY")


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


class Topics(BaseModel):
    topic: str = Field(..., description="Topic Name if found")
    definitions: str = Field(..., description="definition found in topic")
    PositiveConcepts: str = Field(...,
                                  description="positive facts found in topic")
    NegativeConcepts: str = Field(..., description="negative found in topic")
    links: List[str] = Field(..., description="Links found in topic")
    challenges: str = Field(..., description="challenges found in topic")
    summaryTopic: str = Field(..., description="summary of the topic")


class Content(BaseModel):
    name: str = Field(..., description="title of the webpage")
    summary: str = Field(..., description="summary of the text")
    challenges: str = Field(
        ..., description="most difficult challenges found by the author in the text")
    Topics: str = List[Topics]


GHtool = GithubSearchTool(
    gh_token=GHKEY,
    content_types=['code', 'issue', 'repo']  # Options: code, repo, pr, issue
)

# Creating Agents
scraper_agent = Agent(
    config=agents_config['scraper_agent'],
    tools=[GHtool],
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
    output_file='github2.md'
)

organize_task = Task(
    config=tasks_config['organize'],
    agent=organizer_agent,
    context=[scrape_task],
    output_pydantic=Content,
)

# Creating Crew
GHScrape = Crew(
    agents=[
        scraper_agent,
        organizer_agent,
    ],
    tasks=[
        scrape_task,
    ],
    verbose=True
)

topic = {'topic': 'ecole 42, piscine. Sample: https://github.com/evgenkarlson/COMPLETED_PISCINE_C'}
result = GHScrape.kickoff(inputs=topic)

print(result.dict())  # Pydantic v1
print(result.model_dump())  # Pydantic v2
