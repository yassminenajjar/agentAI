import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from root directory
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

class Config:
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
    
    # Database Configuration
    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    DB_SERVER = os.getenv("DB_SERVER")  # YASSMINENAJJAR\SQLSERVER2022
    DB_DATABASE = os.getenv("DB_DATABASE")  # WireBreak
    DB_TRUSTED_CONNECTION = os.getenv("DB_TRUSTED_CONNECTION", "yes")

    @property
    def db_connection_string(self):
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_SERVER};"
            f"DATABASE={self.DB_DATABASE};"
            f"Trusted_Connection={self.DB_TRUSTED_CONNECTION};"
        )

config = Config()