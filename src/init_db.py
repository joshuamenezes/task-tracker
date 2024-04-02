import sqlite3

# Connect to SQLite database (creates a new database if it doesn't exist)
conn = sqlite3.connect('task_db.sqlite')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create Tasks table
cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
                    id INTEGER UNSIGNED PRIMARY KEY NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date DATETIME,
                    priority INTEGER UNSIGNED ,
                    tag TEXT
                )''')
conn.commit()
conn.close()
