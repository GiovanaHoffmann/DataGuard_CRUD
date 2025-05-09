import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

class Database:
    def __init__(self):
        self.config = {
            "database": os.getenv("DB_NAME", "client_governance"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "postgres"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }
        self.conn = None

    def connect(self):
        try:
            if self.conn is None or self.conn.closed:
                self.conn = psycopg2.connect(**self.config)
            return self.conn
        except OperationalError as e:
            raise Exception(f"Erro de conexão: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()