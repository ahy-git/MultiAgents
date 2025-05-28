import os
import pandas as pd 
from crew_query import SQLQueryCrew
from postgres_connection import PostgresConnection
from postgres_db import PostgresDB

# schemas path
root = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(root,"schemas", "schema_ecommerce.yaml")

sql_crew = SQLQueryCrew()

inputs = {
    "database_type": "Postgres",
    "database_name": "ecommerce",
    "yaml_path": schema_path,
    "user_request": "Qual é o nome e o preço dos produtos que custam menos de R$ 100. Eu só quero os 5 primeiros resultados.",
    "json_output": False
}

sql_query = sql_crew.kickoff(inputs)

print("\n🔍 Consulta SQL Gerada:\n")
print(sql_query)

ecommerce_database = PostgresDB.ECOMMERCE
conn = PostgresConnection(db_uri=ecommerce_database)
conn.connect()

print (conn.get_current_database())

cursor = conn.cursor
cursor.execute(sql_query)

results = cursor.fetchall()

colunas = conn.get_colunas()

df = pd.DataFrame(results, columns=colunas)

conn.disconnect()

if results:
    print(df)
else:
    print("Nothing found")