class AuditLog:
    def __init__(self, db):
        self.db = db

    def log_change(self, user_action, table_name, record_id, old_data=None, new_data=None):
        cursor = self.db.conn.cursor()
        cursor.execute(
            """INSERT INTO audit_log 
            (user_action, table_name, record_id, old_data, new_data) 
            VALUES (%s, %s, %s, %s, %s)""",
            (user_action, table_name, record_id, old_data, new_data)
        )
        self.db.conn.commit()