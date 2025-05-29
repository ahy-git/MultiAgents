import os
import json
import tempfile
import pandas as pd
import csv
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM
from toolPandasTools import PandasQueryTool
from toolDuckDBQuery import DuckDBQueryTool


class DataQueryCrew:
    def __init__(self, file_path: str):
        self.llm = MyLLM.Ollama_qwen3
        self.llmtools=MyLLM.Ollama_devstral
        self.file_path, self.columns = self._preprocess_data(file_path)
        self.pandas_tool = PandasQueryTool()
        self.duckdb_tool = DuckDBQueryTool(csv_path=self.file_path)
        self.crew = self._setup_crew()

    def _preprocess_data(self, file_path):
        df = pd.read_csv(file_path, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])

        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)

        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            df.to_csv(temp_file.name, index=False, quoting=csv.QUOTE_ALL)
            return temp_file.name, df.columns.tolist()

    def _setup_crew(self):
        # Agents
        planner = Agent(
            role="Query Strategy Planner",
            goal="Identify the best tool and query strategy for user question",
            backstory="Expert in selecting optimal data querying tools based on question type.",
            llm=self.llm,
            verbose=True
        )

        executor = Agent(
            role="Query Executor",
            goal="Execute SQL or Pandas query on the sample.csv and return the result",
            backstory="Expert in executing precise data queries and returning clean results.",
            tools=[self.pandas_tool, self.duckdb_tool],
            llm=self.llm,
            verbose=True
        )

        explainer = Agent(
            role="Insights Communicator",
            goal="Provide a human-readable explanation using the executed result",
            backstory="Expert in explaining technical data results in accessible language.",
            llm=self.llm,
            verbose=True
        )

        # Tasks
        task1 = Task(
            description=(
                "Analyze the following user question: {question}\n"
                "Decide whether it should be answered using SQL (DuckDBQueryTool) or Pandas (PandasQueryTool).\n"
                "Create the most appropriate query and describe which tool should be used."
                "You know that the table is '{table_name}' and contains the field: {columns}"
            ),
            expected_output="JSON block with tool name and query string",
            agent=planner
        )

        task2 = Task(
            description=(
                "You will receive a tool name and query.\n"
                "Execute the query using the correct tool.\n"
                "Return ONLY the raw result of the tool execution as JSON."
            ),
            expected_output="JSON block with query result",
            agent=executor
        )

        task3 = Task(
            description=(
                "Given the tool used, the query, and its result, write a final answer.\n"
                "Structure output with:\n"
                "1. Reasoning\n2. Query Used\n3. Result\n4. Final Answer"
            ),
            expected_output="Markdown block with natural-language answer based on result",
            agent=explainer
        )

        return Crew(
            agents=[planner, executor, explainer],
            tasks=[task1, task2, task3],
            process=Process.sequential
        )

    def kickoff(self, question: str) -> str:
        return self.crew.kickoff(inputs={"question": question,
                                         "columns":self.columns,
                                         "table_name" :"sample"
                                         })


if __name__ == "__main__":
    file_path = "sample.csv"
    question = "Quantos funcionários ganham acima de 60 mil?"

    if not os.path.exists(file_path):
        raise FileNotFoundError("sample.csv not found. Please provide a valid CSV file.")

    dq = DataQueryCrew(file_path)
    result = dq.kickoff(question)
    print("\n🔍 SQL Query Result:\n")
    print(result.raw if hasattr(result, "raw") else result)
