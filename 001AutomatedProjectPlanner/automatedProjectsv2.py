import pandas as pd
import warnings
import os
import sys
import yaml
import logging
import json
import datetime
from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew
from config.helper import load_env
from config.llm_models import llm_models

# Configuração de logs para garantir verbose no terminal
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Carregar variáveis de ambiente
warnings.filterwarnings('ignore')
load_env()

model1 = "geminiflash"
model2 = model1
model3 = model1

# Carregar configurações YAML
config_files = {"agents": 'config/agents.yaml', "tasks": 'config/tasks.yaml'}
configs = {name: yaml.safe_load(open(path, 'r'))
           for name, path in config_files.items()}

# Definição de modelos Pydantic


class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    estimated_time_hours: float = Field(
        ..., description="Estimated time to complete the task in hours")
    required_resources: List[str] = Field(
        ..., description="List of resources required to complete the task")
    risks_uncertainties: List[str] = Field(
        ..., description="List risks associated in the task")


class Milestone(BaseModel):
    milestone_name: str = Field(..., description="Name of the milestone")
    tasks: List[str] = Field(...,
                             description="List of task IDs associated with this milestone")
    risks_milestone: List[str] = Field(...,
                                       description="List of risks associated with this milestone")


class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(
        default_factory=list, description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(
        default_factory=list, description="List of project milestones")


# Criar agentes
agents = {
    "planning": Agent(config=configs['agents']['project_planning_agent'], llm=llm_models.get_model(model1)),
    "estimation": Agent(config=configs['agents']['estimation_agent'], llm=llm_models.get_model(model2)),
    "resource": Agent(config=configs['agents']['resource_allocation_agent'], llm=llm_models.get_model(model3))
}

# Criar tarefas
tasks = {
    "breakdown": Task(config=configs['tasks']['task_breakdown'], agent=agents['planning']),
    "estimation": Task(config=configs['tasks']['time_resource_estimation'], agent=agents['estimation']),
    "allocation": Task(config=configs['tasks']['resource_allocation'], agent=agents['resource'], output_pydantic=ProjectPlan)
}

# Criar a equipe (Crew)
crew = Crew(agents=list(agents.values()),
            tasks=list(tasks.values()), verbose=True)

# Carregar entradas do projeto de um arquivo externo
input_file = 'config/project_inputs.json'
with open(input_file, 'r') as f:
    inputs = json.load(f)

# Registrar timestamps de início e fim
start_time = datetime.datetime.now()
logging.info(f"Execution started at: {start_time}")

# Executar o CrewAI
logging.info("Running CrewAI...")
result = crew.kickoff(inputs=inputs)
logging.info("CrewAI Execution Completed.")


end_time = datetime.datetime.now()
logging.info(f"Execution finished at: {end_time}")

# Determinar nome do arquivo de saída
output_base = "execution_output"
output_ext = ".md"
output_file = f"{output_base}{output_ext}"
counter = 1
while os.path.exists(output_file):
    output_file = f"{output_base}_{counter}{output_ext}"
    counter += 1
print(crew.usage_metrics)


# Verificar e converter `crew.usage_metrics` para um dicionário antes de serializar
usage_metrics_dict = crew.usage_metrics.model_dump() if hasattr(
    crew.usage_metrics, "dict") else {}

# Capturar os modelos usados por cada agente
agent_models = {name: agent.llm.model for name, agent in agents.items()}



# Gerar saída em arquivo Markdown
with open(output_file, "w") as f:
    f.write(f"# CrewAI Execution Report\n\n")
    f.write(f"## Token Usage Metrics\n")
    f.write(f"```json\n{json.dumps(usage_metrics_dict, indent=4)}\n```\n\n")
    f.write(f"## Models Used per Agent\n")
    f.write(f"```json\n{json.dumps(agent_models, indent=4)}\n```\n\n")
    f.write(f"**Start Time:** {start_time}\n\n")
    f.write(f"**End Time:** {end_time}\n\n")
    f.write(f"## Input Data\n")
    f.write(f"```json\n{json.dumps(inputs, indent=4)}\n```\n\n")
    f.write(f"## Execution raw result\n")
    f.write(f"```\n{result}\n```\n")
    # Adding formatted project plan details
    f.write(f"## Project Plan\n")
    f.write(f"## Tasks\n")
    f.write(f"## Milestones\n")



# Exibir a saída da execução
print(f"CrewAI Execution Completed. Output saved in {output_file}")
print(crew.usage_metrics)
print(usage_metrics_dict)


costs = 0.150 * (crew.usage_metrics.prompt_tokens +
                 crew.usage_metrics.completion_tokens) / 1_000_000
print(f"Total costs: ${costs:.4f}")

# Convert UsageMetrics instance to a DataFrame
df_usage_metrics = pd.DataFrame([crew.usage_metrics.model_dump()])
df_usage_metrics

result.pydantic.model_dump_json()
milestones = result.pydantic.model_dump_json()['milestones']
tasks = result.pydantic.model_dump_json()['tasks']

df_tasks = pd.DataFrame(tasks)
print("Tasks:")
print(tasks)


# Display the DataFrame as an HTML table
df_tasks.style.set_table_attributes('border="1"').set_caption("Task Details").set_table_styles(
    [{'selector': 'th, td', 'props': [('font-size', '120%')]}]
)


df_milestones = pd.DataFrame(milestones)

print("Milestones:")
print(milestones)

# Display the DataFrame as an HTML table
df_milestones.style.set_table_attributes('border="1"').set_caption("Task Details").set_table_styles(
    [{'selector': 'th, td', 'props': [('font-size', '120%')]}]
)
