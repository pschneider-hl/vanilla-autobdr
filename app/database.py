import sqlite3
from datetime import datetime

DB_PATH = "autobdr.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for logging each email sent
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id TEXT,
        email TEXT,
        persona TEXT,
        subject TEXT,
        message TEXT,
        attempt INTEGER,
        timestamp TEXT,
        outcome TEXT DEFAULT 'sent'
    );
    """)

