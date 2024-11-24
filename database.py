import sqlite3
from datetime import datetime

class DatabaseLogger:
    def __init__(self, db_path="sync_log.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)  # Добавляем check_same_thread
        self.create_log_table()


    def create_log_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    path TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def log_action(self, action, path):
        path = path.replace("/", "\\")
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO logs (action, path) VALUES (?, ?)", (action, path))

