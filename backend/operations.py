from backend.data_quality import DataQuality
from datetime import datetime
import json

class ClientOperations:
    def __init__(self, db):
        self.db = db
        if not self.db.conn or self.db.conn.closed:
            self.db.connect()  # Garante conexão ativa

    def insert(self, nome, sobrenome, email, cpf):
        """Insere cliente assumindo que CPF já foi validado no frontend"""
        cursor = self.db.conn.cursor()
        try:
            nome = DataQuality.normalize_name(nome)
            sobrenome = DataQuality.normalize_name(sobrenome)
            cpf = DataQuality.normalize_cpf(cpf)

            cursor.execute(
                """INSERT INTO clientes 
                (nome, sobrenome, email, cpf) 
                VALUES (%s, %s, %s, %s) RETURNING id""",
                (nome, sobrenome, email, cpf)
            )
            client_id = cursor.fetchone()[0]
            
            self._log_operation(
                operation="INSERT",
                table_name="clientes",
                record_id=client_id,
                new_values={
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": DataQuality.anonymize_data(email, 3),
                    "cpf": DataQuality.anonymize_data(cpf)
                }
            )
            self.db.conn.commit()
            return client_id
        except Exception as e:
            self.db.conn.rollback()
            raise e

    def _log_operation(self, operation, table_name, record_id, old_values=None, new_values=None):
        """Registra operações na tabela de auditoria com anonimização automática de PII"""
        def anonymize_if_pii(data):
            if not data:
                return None
            return {
                field: DataQuality.anonymize_data(value) if DataQuality.is_pii_field(field) 
                    else value
                for field, value in data.items()
            }

        cursor = self.db.conn.cursor()
        cursor.execute(
            """INSERT INTO audit_log 
            (operacao, tabela, id_registro, dados_antigos, dados_novos) 
            VALUES (%s, %s, %s, %s, %s)""",
            (operation, table_name, record_id, 
            json.dumps(anonymize_if_pii(old_values)) if old_values else None, 
            json.dumps(anonymize_if_pii(new_values)) if new_values else None)
        )

    def view(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY nome, sobrenome")
        return cursor.fetchall()

    def search(self, nome="", sobrenome="", email="", cpf=""):
        cursor = self.db.conn.cursor()
        cursor.execute(
            """SELECT * FROM clientes 
            WHERE nome ILIKE %s OR sobrenome ILIKE %s 
            OR email ILIKE %s OR cpf LIKE %s
            ORDER BY nome, sobrenome""",
            (f"%{nome}%", f"%{sobrenome}%", f"%{email}%", f"%{cpf}%")
        )
        return cursor.fetchall()

    def update(self, id, nome, sobrenome, email, cpf):
        cursor = self.db.conn.cursor()
        try:
            # Pega valores atuais para auditoria
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
            old_values = cursor.fetchone()

            # Normaliza novos valores
            nome = DataQuality.normalize_name(nome)
            sobrenome = DataQuality.normalize_name(sobrenome)
            cpf = DataQuality.normalize_cpf(cpf)

            cursor.execute(
                """UPDATE clientes 
                SET nome = %s, sobrenome = %s, email = %s, cpf = %s 
                WHERE id = %s""",
                (nome, sobrenome, email, cpf, id)
            )

            self._log_operation(
                operation="UPDATE",
                table_name="clientes",
                record_id=id,
                old_values={
                    "nome": old_values[1],
                    "sobrenome": old_values[2],
                    "email": DataQuality.anonymize_data(old_values[3], 3),
                    "cpf": DataQuality.anonymize_data(old_values[4])
                },
                new_values={
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": DataQuality.anonymize_data(email, 3),
                    "cpf": DataQuality.anonymize_data(cpf)
                }
            )
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            raise e

    def delete(self, id):
        cursor = self.db.conn.cursor()
        try:
            # Soft delete (marca como inativo)
            cursor.execute(
                "UPDATE clientes SET ativo = FALSE WHERE id = %s",
                (id,)
            )
            self._log_operation(
                operation="DELETE",
                table_name="clientes",
                record_id=id
            )
            self.db.conn.commit()
        except Exception as e:
            self.db.conn.rollback()
            raise e