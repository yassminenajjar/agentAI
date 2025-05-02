import pyodbc
from Config import config

class Database:
    def __init__(self):
        self.connection_string = config.db_connection_string
    
    def get_connection(self):
        """Establish and return a database connection"""
        try:
            conn = pyodbc.connect(self.connection_string)
            return conn, conn.cursor()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")
    
    def init_app(self, app):
        """Initialize with Flask app context"""
        app.teardown_appcontext(self.close_connection)
    
    def close_connection(self, exception=None):
        """Close connection on app teardown"""
        pass

# Singleton instance
db_instance = Database()