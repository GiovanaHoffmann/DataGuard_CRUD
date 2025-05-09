from backend.database import Database
from backend.models import create_tables

def initialize():
    db = Database()
    try:
        db.connect()
        create_tables(db)
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    initialize()