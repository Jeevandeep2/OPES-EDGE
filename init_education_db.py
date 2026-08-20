import sqlite3
import os

# ============================================================
# OPES EDGE - EDUCATION DATABASE INITIALIZATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

print("Using database:")
print(DATABASE)

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ============================================================
# COURSES TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    subject TEXT,
    category TEXT,
    instructor TEXT,
    duration TEXT,
    level TEXT,
    image_url TEXT,
    course_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ============================================================
# STUDY MATERIALS TABLE
# ============================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS study_materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    subject TEXT,
    material_type TEXT,
    file_url TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# ============================================================
# VERIFY TABLES
# ============================================================

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name
""")

tables = cursor.fetchall()

print("\nDatabase tables:")

for table in tables:
    print(" -", table[0])

# ============================================================
# VERIFY EDUCATION TABLES
# ============================================================

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name IN ('courses', 'study_materials')
ORDER BY name
""")

education_tables = cursor.fetchall()

print("\nEducation tables:")

for table in education_tables:
    print(" -", table[0])

if len(education_tables) == 2:
    print("\nSUCCESS: Education database is ready.")
else:
    print("\nERROR: Education tables were not created.")

conn.close()
