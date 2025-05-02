import pandas as pd
from app.models.database import db_instance

class SQLService:
    def __init__(self):
        self.conn, self.cursor = db_instance.get_connection()
        self.schema_info = self._get_schema_info()
    
    def _get_schema_info(self):
        """Retrieve the database schema information"""
        self.cursor.execute("""
            SELECT t.name AS table_name, c.name AS column_name, ty.name AS type_name
            FROM sys.tables t
            JOIN sys.columns c ON t.object_id = c.object_id
            JOIN sys.types ty ON c.user_type_id = ty.user_type_id
            ORDER BY t.name, c.column_id
        """)
        schema = {}
        for table, column, dtype in self.cursor.fetchall():
            schema.setdefault(table, []).append(f"{column} ({dtype})")
        return "\n".join([f"{table}({', '.join(cols)})" for table, cols in schema.items()])
    
    def execute_query(self, sql_query):
        """Execute a SQL query and return results as a DataFrame"""
        try:
            self.cursor.execute(sql_query)
            columns = [column[0] for column in self.cursor.description]
            results = self.cursor.fetchall()
            return pd.DataFrame.from_records(results, columns=columns)
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def get_schema(self):
        """Return the database schema"""
        return self.schema_info