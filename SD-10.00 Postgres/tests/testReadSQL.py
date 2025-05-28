# Cria as base de dados referentes aos arquivos clinica.sql e ecommerce.sql 
# Executa os scripts

import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
# Configurações de conexão (ajuste conforme seu ambiente)
base_uri = os.getenv("DATABASE_URI")
ADMIN_DB_URI =  f"{base_uri}/postgres"

DATABASES = {
    "clinica": "clinica.sql",
    "ecommerce": "ecommerce.sql"
}

def create_database_if_not_exists(conn, db_name):
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE "{db_name}"')
            print(f"[INFO] Banco de dados '{db_name}' criado com sucesso.")
        else:
            print(f"[INFO] Banco de dados '{db_name}' já existe.")

def execute_sql_file(db_uri, sql_file_path):
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    with psycopg2.connect(db_uri) as conn:
        with conn.cursor() as cur:
            for statement in sql.split(';'):
                stmt = statement.strip()
                if stmt:
                    cur.execute(stmt)
        conn.commit()
        print(f"[INFO] Script '{sql_file_path}' executado com sucesso no banco.")

if __name__ == "__main__":
    admin_conn = None
    
    try:
        print("[INFO] Conectando ao banco administrativo...")
        admin_conn = psycopg2.connect(ADMIN_DB_URI)

        for db_name, sql_file in DATABASES.items():
            create_database_if_not_exists(admin_conn, db_name)

            # Gera URI do banco específico
            db_uri = ADMIN_DB_URI.replace("/postgres", f"/{db_name}")
            print(f"[INFO] Executando script para o banco '{db_name}'...")
            execute_sql_file(db_uri, sql_file)

    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        if admin_conn is not None:
            admin_conn.close()
