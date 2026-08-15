import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Phase 1 tables
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Phase 2 tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            experience_years TEXT,
            location TEXT NOT NULL,
            preferred_language TEXT DEFAULT 'English',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL,
            crop_category TEXT NOT NULL,
            sowing_date TEXT,
            expected_harvest_date TEXT,
            area TEXT,
            soil_type TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized at:", DATABASE)

if __name__ == '__main__':
    init_db()