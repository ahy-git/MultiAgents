import psycopg2
# from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

class PostgresConnection:
    def __init__(self, db_uri=None):
        
        self.conn = None
        self.cursor = None
        self.db_uri = db_uri
    
    def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_uri)
            self.cursor = self.conn.cursor()
            print("[PostgresConnection] Conexão estabelecida com sucesso")
        except Exception as e:
            print(f"[PostgresConnection] Erro ao conectar: {str(e)}")
            self.conn = None
            self.cursor = None            
    
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def get_current_database(self):
        if not self.conn:
            raise ConnectionError("Connection not established")
        self.cursor.execute("SELECT current_database();")
        return self.cursor.fetchone()[0]
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
    
    def get_colunas(self):
        if not self.cursor:
            raise ConnectionError("Cursor not defined")
        return [desc[0] for desc in self.cursor.description]