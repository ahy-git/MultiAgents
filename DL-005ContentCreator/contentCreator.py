# Warning control 
# Lite LLLM upgraded from 1.50.4 to 1.63.2
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
from config.helper import load_env
load_env()
import litellm
import os
import yaml
from crewai import Agent, Task, Crew

from pydantic import BaseModel, Field
from typing import List

litellm.set_verbose=True

class SocialMediaPost(BaseModel):
    platform: str = Field(..., description="The social media platform where the post will be published (e.g., Twitter, LinkedIn).")
    content: str = Field(..., description="The content of the social media post, including any hashtags or mentions.")

class ContentOutput(BaseModel):
    article: str = Field(..., description="The article, formatted in markdown.")
    social_media_posts: List[SocialMediaPost] = Field(..., description="A list of social media posts related to the article.")
    

# Define file paths for YAML configurations
files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)
agents_config = configs['agents']
tasks_config = configs['tasks']

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from config.llm_models import llm_models

groq_llm = llm_models.get_model('groqllama33vers')
llm2 = llm_models.get_model('groqllama33vers')

# Creating Agents
market_news_monitor_agent = Agent(
    config=agents_config['market_news_monitor_agent'],
    tools=[SerperDevTool(), ScrapeWebsiteTool()],
    llm=groq_llm,
)

data_analyst_agent = Agent(
    config=agents_config['data_analyst_agent'],
    tools=[SerperDevTool(), WebsiteSearchTool()],
    llm=groq_llm,
)

content_creator_agent = Agent(
    config=agents_config['content_creator_agent'],
    tools=[SerperDevTool(), WebsiteSearchTool()],
    llm=llm2
)

quality_assurance_agent = Agent(
    config=agents_config['quality_assurance_agent'],
    llm=llm2

)

# Creating Tasks
monitor_financial_news_task = Task(
    config=tasks_config['monitor_financial_news'],
    agent=market_news_monitor_agent
)

analyze_market_data_task = Task(
    config=tasks_config['analyze_market_data'],
    agent=data_analyst_agent
)

create_content_task = Task(
    config=tasks_config['create_content'],
    agent=content_creator_agent,
    context=[monitor_financial_news_task, analyze_market_data_task]
)

quality_assurance_task = Task(
    config=tasks_config['quality_assurance'],
    agent=quality_assurance_agent,
    output_pydantic=ContentOutput
)

# Creating Crew
content_creation_crew = Crew(
    agents=[
        market_news_monitor_agent,
        data_analyst_agent,
        content_creator_agent,
        quality_assurance_agent
    ],
    tasks=[
        monitor_financial_news_task,
        analyze_market_data_task,
        create_content_task,
        quality_assurance_task
    ],
    verbose=True
)

result = content_creation_crew.kickoff(inputs={
  'subject': 'Inflation in the Brazil in 2025 and impact to South America'
})

import textwrap

posts = result.pydantic.dict()['social_media_posts']
for post in posts:
    platform = post['platform']
    content = post['content']
    print(platform)
    wrapped_content = textwrap.fill(content, width=50)
    print(wrapped_content)
    print('-' * 50)
    
from IPython.display import display, Markdown
display(Markdown(result.pydantic.dict()['article']))