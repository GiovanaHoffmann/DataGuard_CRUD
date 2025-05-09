def create_tables(db):
    cursor = db.conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            cpf TEXT UNIQUE NOT NULL CHECK (LENGTH(cpf) = 11),
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP,
            ativo BOOLEAN DEFAULT TRUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            operacao VARCHAR(20) NOT NULL,
            tabela VARCHAR(50) NOT NULL,
            id_registro INTEGER NOT NULL,
            dados_antigos JSONB,
            dados_novos JSONB,
            executado_por VARCHAR(100) DEFAULT CURRENT_USER,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    db.conn.commit()