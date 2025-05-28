import os
import yaml
from psycopg2 import sql
from postgres_connection import PostgresConnection
from postgres_db import PostgresDB

class SchemaTool:
    """
    Extrai informacoes do schema e gera YAMLs
    """
    
    def __init__(self, db_uri,cat_columns=None):
        """
        Initialize with db URI and dic of the catgorical columns

        Args:
            db_uri (_type_): self explanatory
            category_columns (_type_, optional): self explanatory. Defaults to None.
        """
        
        self.db = PostgresConnection(db_uri)
        self.categorical_columns = cat_columns if cat_columns else {}
    
    def connect(self):
        self.db.connect()
        
    def disconnect(self):
        self.db.disconnect()
        
    def list_tables_and_columns(self):
        """
        Return a dic with tables, columns and possible values (categories)
        """
        sql_query = """
                SELECT 
            table_schema,
            table_name,
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY table_schema, table_name, ordinal_position;
        """
        cursor = self.db.cursor
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        
        schema_info={}
        for schema, table, column, dtype, nullable in rows:
            if schema not in schema_info:
                schema_info[schema]={}
            if table not in schema_info[schema]:
                schema_info[schema][table] = []
                
            column_def = {
                "column_name" : column,
                "data_type" : dtype,
                "is_nullable" : nullable
            }
            
            # Busca valores distintos
            if table in self.categorical_columns and column in self.categorical_columns[table]:
                distinct_vals = self.get_distinct_values(schema,table,column)
                if distinct_vals:
                    column_def["possible_values"] = distinct_vals
            schema_info[schema][table].append(column_def)
        return schema_info
    
    def get_distinct_values(self,schema,table,column,limit=50):
        """
        Retrieve distinct values of a categorical column and includes ID
        """
        
        # Finds out the primary key
        primary_key = self.get_primary_key(schema,table)
        if not primary_key:
            print(f"No primary key found in {table}")
            return []
        
        sql_query =sql.SQL( 
        """
        SELECT {primary_key}, {column}
        FROM {schema}.{table}
        WHERE {column} IS NOT NULL
        ORDER BY {primary_key}
        LIMIT {limit};
        """).format(
            primary_key=sql.Identifier(primary_key),
            column=sql.Identifier(column),
            schema=sql.Identifier(schema),
            table=sql.Identifier(table),
            limit=sql.Literal(limit)
        )
    
        cursor = self.db.cursor
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        
        # Values converted to UTF-8 and correctly structured
        return [{"id": row[0], column: str(row[1])} for row in rows]
    
    def get_primary_key(self,schema,table):
        
        sql_query=sql.SQL("""
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = {schema}
          AND tc.table_name = {table};            
        """
        ).format(
            schema=sql.Literal(schema),
            table=sql.Literal(table))
        
        cursor = self.db.cursor 
        cursor.execute(sql_query)
        
        result = cursor.fetchone()
        return result[0] if result else None
    
    def generate_yaml(self):
        
        database_name = self.db.get_current_database()
        tables_info = self.list_tables_and_columns()
        
        final_data = {
            "tables" : tables_info
        }
        
        output_folder = os.path.join(os.getcwd(),"schemas")
        os.makedirs(output_folder,exist_ok=True)
        output_file = os.path.join(output_folder,f"schema_{database_name}.yaml")
        
        with open(output_file, "w", encoding="utf-8") as yaml_file:
            yaml.dump(final_data, yaml_file,sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"YAML created successfully: {output_file}")
    
    def generateschema(self):
        try:
            print("Connecting do db...")
            self.connect()
            print("Creating YAML...")
            self.generate_yaml()
        except Exception as e:
            print(f"Error during Schema generation: {e}")
        finally:
            print("Disconnecting database...")
            self.disconnect()
            print("Process ended.")
            
   