from .constants import DB_PATH
from datetime import datetime
import sqlite3
from ..models.task import Task


class TaskDAO:
    """
    The DAO (Data Access Object) acts as a consolidated interface to interact
    with the database.
    """

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Connects to the database
        """
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        """
        Disconnects from the database
        """
        try:
            self.conn.close()
        except Exception as e:
            print(f"Error disconnecting from the database: {e}")

    def create_task(self, task: Task) -> int:
        """
        Creates a given task in the database
        :param task: The task to create
        :return: The ID of the newly created task
        """
        self.connect()

        self.cursor.execute(
            '''INSERT INTO Tasks (title, description, due_date, priority, tag)
                                VALUES (?, ?, ?, ?, ?)''',
            (task.title,
             task.description,
             task.due_date,
             task.priority,
             task.tag))
        self.conn.commit()
        task_id = self.cursor.lastrowid
        self.disconnect()

        return task_id

    def get_task(self, task_id):
        """
        Selects a single task with the given id (if it exists)
        :param task_id: The id of the task we wish to retrieve
        :return: The task itself
        """
        self.connect()
        self.cursor.execute("SELECT * FROM Tasks WHERE id = ?", (task_id,))
        task = self.cursor.fetchall()
        self.disconnect()
        return task

    def get_all_tasks(self):
        """
        Gets all tasks in the database
        :return: All tasks in the database
        """
        self.connect()
        self.cursor.execute("SELECT * FROM Tasks")
        tasks = self.cursor.fetchall()
        self.disconnect()
        return tasks

    def update_task(self, task_id, title=None, description=None, due_date=None,
                    priority=None, tag=None):
        """
        Updates a given task with the supplied information.
        """
        self.connect()
        # Construct the UPDATE query dynamically based on the supplied
        # parameters
        update_query = "UPDATE Tasks SET"
        update_values = []

        if title is not None:
            update_query += " title=?,"
            update_values.append(title)
        if description is not None:
            update_query += " description=?,"
            update_values.append(description)
        if due_date is not None:
            update_query += " due_date=?,"
            update_values.append(due_date)
        if priority is not None:
            update_query += " priority=?,"
            update_values.append(priority)
        if tag is not None:
            update_query += " tag=?,"
            update_values.append(tag)

        # Remove the trailing comma and add WHERE clause
        update_query = update_query.rstrip(",") + " WHERE id=?"
        update_values.append(task_id)

        # Execute the UPDATE query
        self.cursor.execute(update_query, tuple(update_values))
        self.conn.commit()
        self.disconnect()

    def delete_task(self, task_id):
        """
        Deletes a task
        :param task_id: The ID of the task we wish to delete
        """
        self.connect()
        self.cursor.execute("DELETE FROM Tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        self.disconnect()
