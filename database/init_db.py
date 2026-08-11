import sqlite3
import os

# This file lives in the database/ folder
# We want the database file to be created in the main project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def init_db():
    """
    Creates the SQLite database and tables if they don't exist.
    Run this once before starting the app for the first time.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users table: stores login information for the platform
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'citizen',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Contacts table: stores messages from the "Contact Us" or CTA forms
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully at:", DATABASE)

if __name__ == '__main__':
    init_db()