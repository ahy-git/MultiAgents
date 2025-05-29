# toolDuckDBQuery.py
import os
import duckdb
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class DuckDBQueryInput(BaseModel):
    sql: str = Field(..., description="SQL query to execute on the CSV data loaded into DuckDB")


class DuckDBQueryTool(BaseTool):
    name: str = "DuckDB Query Tool"
    description: str = "Executes SQL queries on a sample CSV using DuckDB in-memory."
    args_schema: Type[BaseModel] = DuckDBQueryInput

    def _run(self, sql: str) -> str:
        try:
            # Load CSV into DuckDB
            csv_path = os.path.join(os.path.dirname(__file__), "sample.csv")
            conn = duckdb.connect(database=":memory:")
            conn.execute(f"CREATE TABLE sample AS SELECT * FROM read_csv_auto('{csv_path}')")

            # Execute user query
            result = conn.execute(sql).fetchdf()

            if result.empty:
                return "Query executed successfully. No rows returned."
            # return result.to_json(orient='records')
            return {"result": str(result.iloc[0, 0])}
            
        except Exception as e:
            return f"Error executing DuckDB query: {e}"

if __name__ == "__main__":
    tool = DuckDBQueryTool()

    print("\n🔍 Test Query 1: All data")
    print(tool.run(sql="SELECT * FROM sample"))

    print("\n🔍 Test Query 2: Filter salary > 55000")
    print(tool.run(sql="SELECT name, salary FROM sample WHERE salary > 55000"))
