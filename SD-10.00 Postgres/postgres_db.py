import os
from dotenv import load_dotenv

class PostgresDB:
    
    load_dotenv()
    _db_uri = os.getenv("DATABASE_URI","").rstrip("/")
    
    if not _db_uri:
        raise ValueError("DATABASE_URI not defined in .env")
    
    #dics
    _databases = {
        "ecommerce" : f"{_db_uri}/ecommerce",
        "clinica" : f"{_db_uri}/clinica",
        "evolution": f"{_db_uri}/evolution"
    }
    
    @staticmethod
    def get_database_uri(name: str):
        "Return DB uri based on provided name"
        name = name.lower()
        if name not in PostgresDB._databases:
            raise ValueError("Base '{name}' not found. Pick between: {list(PostgresDB._databases.keys())}")
        return PostgresDB._databases[name]
    
    @staticmethod
    def __getitem__(name:str):
        return PostgresDB.get_database_uri(name)
    
    ECOMMERCE = _databases["ecommerce"]
    CLINICA = _databases["clinica"]
    EVOLUTION = _databases["evolution"]    
    
        
        