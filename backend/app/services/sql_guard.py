class SQLGuard:

    @staticmethod
    def is_safe(sql: str):
        sql = sql.strip().upper()
        return sql.startswith("SELECT")