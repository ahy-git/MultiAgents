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

model1 = "llama321bdocker"
model2 = model1
model3 = model1

# Carregar configurações YAML
config_files = {"agents": 'config/agents.yaml', "tasks": 'config/tasks.yaml'}
configs = {name: yaml.safe_load(open(path, 'r'))
           for name, path in config_files.items()}


# Definição de modelos Pydantic


class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    task_id: str = Field(..., description="Unique ID for this task")
    estimated_time_hours: float = Field(
        ..., description="Estimated time to complete the task in hours")
    required_resources: List[str] = Field(
        ..., description="List of resources required to complete the task")
    risks_task: List[str] = Field(
        ..., description="List risks associated in the task")
    mitigation_task: List[str] = Field(
        ..., description="List mitigations of the risks associated in the task")
    dependencies: List[str] = Field(
        ..., description="List of mandatory tasks done before this task")
    


class Milestone(BaseModel):
    milestone_name: str = Field(..., description="Name of the milestone")
    milestone_name: str = Field(..., description="Unique ID of this milestone")
    tasks: List[str] = Field(...,
                             description="List of task IDs associated with this milestone")
    risks_milestone: List[str] = Field(...,
                                       description="List of risks associated with this milestone")

class GanttChart(BaseModel):
    title: str = Field(..., description="Title of the Gantt chart")
    date_format: str = Field("YYYY-MM-DD", description="Date format used in the chart")
    tasks: List[TaskEstimate] = Field(..., description="List of project tasks")
    milestones: List[Milestone] = Field(..., description="List of project milestones")

    def generate_mermaid(self) -> str:
        """Generate Mermaid Gantt chart syntax from the model."""
        mermaid_code = f"gantt\n    title {self.title}\n    dateFormat {self.date_format}\n"
        
        for task in self.tasks:
            # Calculate duration in days (converting from estimated hours)
            duration_days = max(1, round(task.estimated_time_hours / 8))  # Assuming 8-hour workdays
            
            # Determine start date (if dependent, start after the last dependency)
            if task.dependencies:
                dependency_id = task.dependencies[0]  # Taking the first dependency as reference
                line = f"    {task.task_name} :{task.task_id}, after {dependency_id}, {duration_days}d"
            else:
                line = f"    {task.task_name} :{task.task_id}, {self.start_date}, {duration_days}d"

            mermaid_code += line + "\n"

        # Add milestones
        for milestone in self.milestones:
            milestone_line = f"    {milestone.milestone_name} :milestone, {self.start_date}"
            mermaid_code += milestone_line + "\n"

        return mermaid_code

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(
        default_factory=list, description="List of tasks with their estimates")
    milestones: List[Milestone] = Field(
        default_factory=list, description="List of project milestones")
    mermaid_gantt: str = Field(None, description="Pre-generated Mermaid Gantt chart")


model1 = "llama321bdocker"
model2 = model1
model3 = model1

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
    # "allocation": Task(config=configs['tasks']['resource_allocation'], agent=agents['resource'], output_pydantic=ProjectPlan)
    "allocation": Task(config=configs['tasks']['resource_allocation'], agent=agents['resource'], output_json=ProjectPlan)
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
agent_models = {name: agent.llm.model for name, agent in agents.items()}
usage_metrics_str = "\n".join(f"{key}: {value}" for key, value in usage_metrics_dict.items())
agent_models_str = "\n".join(f"{key}: {value}" for key, value in agent_models.items())


# Convert CrewOutput to a dictionary
result_dict = result.model_dump()  # Use .model_dump() if it's a Pydantic model

# Convert JSON to formatted string
json_content = json.dumps(result_dict, indent=4)

breakdown_output = result.tasks_output[0]
estimation_output = result.tasks_output[1]

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
    f.write(f"```\n{agent_models_str}\n```\n\n")
    f.write(f"**Start Time:** {start_time}\n\n")
    f.write(f"**End Time:** {end_time}\n\n")
    f.write(f"**Ellapsed Time:** {elapsed_str}\n\n")
    f.write(f"## Input Data\n")
    f.write(f"```json\n{json.dumps(inputs, indent=4)}\n```\n\n")
    f.write(f"## Project Summary\n")
    f.write(f"{breakdown_output}\n\n")
    f.write(f"{estimation_output}\n\n")
    f.write(f"## Project Plan JSON\n\n```json\n{json_content}\n```\n")

