# Simples teste para validar conexao ao postgres

from postgres_connection import PostgresConnection
from postgres_db import PostgresDB


ecommerce_database = PostgresDB.EVOLUTION

conn = PostgresConnection(db_uri=ecommerce_database)
conn.connect()

print(conn.get_current_database())

cursor = conn.cursor

def run_sql_file(conn, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    
sql_query = 'SELECT * FROM public."Message" ORDER BY id ASC LIMIT 100'

cursor.execute(sql_query)


results = cursor.fetchall()
conn.disconnect()
print(results)



