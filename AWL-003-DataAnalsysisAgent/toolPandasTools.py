# toolPandasTools.py
import os
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class PandasQueryInput(BaseModel):
    query: str = Field(..., description="Python expression using pandas DataFrame variable 'df'")


class PandasQueryTool(BaseTool):
    name: str = "Pandas Query Tool"
    description: str = "Executes pandas expressions on sample CSV data loaded as a DataFrame named 'df'."
    args_schema: Type[BaseModel] = PandasQueryInput

    def _run(self, query: str) -> str:
        try:
            # Load sample.csv from same directory
            csv_path = os.path.join(os.path.dirname(__file__), "sample.csv")
            df = pd.read_csv(csv_path)

            # Clean column names (remove whitespace, lowercase)
            df.columns = df.columns.str.strip().str.lower()

            # Execute query
            result = eval(query)

            if isinstance(result, pd.DataFrame):
                if result.empty:
                    return "Query executed successfully. No rows returned."
                return result.to_markdown(index=False)
            else:
                return str(result)
        except Exception as e:
            return f"Error executing pandas query: {e}"

if __name__ == "__main__":
    tool = PandasQueryTool()

    print("\n🔍 Test 1: Show rows where salary > 55000")
    print(tool.run(query="df[df['salary'] > 55000]"))

    print("\n🔍 Test 2: Average salary")
    print(tool.run(query="df['salary'].mean()"))

    print("\n🔍 Test 3: Count per department")
    print(tool.run(query="df['department'].value_counts()"))
