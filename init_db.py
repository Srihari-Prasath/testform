import sqlite3

conn = sqlite3.connect('data.db')

# Create topics table
conn.execute('''
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year TEXT NOT NULL,
    department_id INTEGER,
    topic TEXT NOT NULL,
    session TEXT,
    selected BOOLEAN NOT NULL DEFAULT 0
)
''')

# Create faculty_details table
conn.execute('''
CREATE TABLE IF NOT EXISTS faculty_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    qualification TEXT NOT NULL,
    experience_nscet INTEGER NOT NULL,
    total_experience INTEGER NOT NULL,
    year TEXT NOT NULL,
    department INTEGER,
    topic TEXT NOT NULL
)
''')

# Create IV_year_data table
conn.execute('''
CREATE TABLE IF NOT EXISTS iv_year_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    forenoon_topic TEXT NOT NULL,
    afternoon_topic TEXT NOT NULL,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    designation TEXT NOT NULL,
    qualification TEXT NOT NULL,
    experience_nscet INTEGER NOT NULL,
    total_experience INTEGER NOT NULL
)
''')

conn.commit()
conn.close()
