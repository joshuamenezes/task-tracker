import sqlite3
from .util.constants import *
import os


def create_db(db_name=DB_NAME):
    # Connect to SQLite database (creates a new database if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create Tasks table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        due_date DATETIME,
                        priority INTEGER UNSIGNED,
                        tag TEXT
                    )''')
    conn.commit()
    conn.close()


def delete_db(db_name=DB_NAME):
    try:
        os.remove(db_name)
        print(f"Database {db_name} deleted successfully.")
    except FileNotFoundError:
        print(f"Database {db_name} does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting the database: {e}")
