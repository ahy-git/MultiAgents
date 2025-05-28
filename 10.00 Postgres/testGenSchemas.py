# generate_all_schemas.py

from schema_generator import SchemaTool
from postgres_db import PostgresDB

# Mapas de colunas categóricas (opcional, customize conforme quiser)
categorical_columns = {
    "clinica": {
        "pacientes": ["sexo"],
        "agendamentos": ["status"],
        "pagamentos": ["status_id"]
    },
    "ecommerce": {
        "pedidos": ["status"],
        "produtos": ["categoria"]
    }
}

def run_schema_generation():
    for db_name in ["clinica", "ecommerce"]:
        print(f"\n[INFO] Gerando YAML para base: {db_name}")
        db_uri = PostgresDB.get_database_uri(db_name)
        cat_cols = categorical_columns.get(db_name, {})
        
        tool = SchemaTool(db_uri=db_uri, cat_columns=cat_cols)
        tool.generateschema()

if __name__ == "__main__":
    run_schema_generation()
