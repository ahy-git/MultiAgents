# Warning control
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
from config.helper import load_env
from config.llm_models import llm_models
load_env()
model1 ='geminiflash'
llm1=llm_models.get_model(model1)

import os
import yaml
from crewai import Agent, Task, Crew

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

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']
from crewai_tools import FileReadTool

csv_tool = FileReadTool(file_path='./support_tickets_data.csv')

# Creating Agents
suggestion_generation_agent = Agent(
  config=agents_config['suggestion_generation_agent'],
  tools=[csv_tool],
  llm=llm1
)

reporting_agent = Agent(
  config=agents_config['reporting_agent'],
  tools=[csv_tool],
  llm=llm1

)

chart_generation_agent = Agent(
  config=agents_config['chart_generation_agent'],
  allow_code_execution=False,
    llm=llm1
)

# Creating Tasks
suggestion_generation = Task(
  config=tasks_config['suggestion_generation'],
  agent=suggestion_generation_agent
)

table_generation = Task(
  config=tasks_config['table_generation'],
  agent=reporting_agent
)

chart_generation = Task(
  config=tasks_config['chart_generation'],
  agent=chart_generation_agent
)

final_report_assembly = Task(
  config=tasks_config['final_report_assembly'],
  agent=reporting_agent,
  context=[suggestion_generation, table_generation, chart_generation]
)


# Creating Crew
support_report_crew = Crew(
  agents=[
    suggestion_generation_agent,
    reporting_agent,
    chart_generation_agent
  ],
  tasks=[
    suggestion_generation,
    table_generation,
    chart_generation,
    final_report_assembly
  ],
  verbose=True
)

support_report_crew.test(n_iterations=1, openai_model_name='gpt-4o-mini')

support_report_crew.train(n_iterations=1, filename='training.pkl')

support_report_crew.test(n_iterations=1, openai_model_name='gpt-4o-mini')

# Display the Trello screenshot
from IPython.display import Image, display

# Load and display the image
test_image = Image(filename='test_before_training.png', width=368)
display(test_image)

result = support_report_crew.kickoff()

from IPython.display import display, Markdown
display(Markdown(result.raw))