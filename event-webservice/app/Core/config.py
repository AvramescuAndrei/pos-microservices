import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_NAME = os.getenv("DB_NAME", "pos_bd")
    DB_USER = os.getenv("DB_USER", "pos_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "pos_user123")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_DRIVER = os.getenv("DB_DRIVER", "pymysql")

settings = Settings()
