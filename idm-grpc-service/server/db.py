import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "db" / "idm.sqlite3"


def get_connection():
    return sqlite3.connect(DB_PATH)
