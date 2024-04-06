from enum import Enum


class Environment(Enum):
    PROD = 'PROD'
    TEST = 'TEST'


DB_PATH = "task-tracker/src/task_db.sqlite"
DB_NAME = "task_db.sqlite"
TEST_DB_NAME = "test_task_db.sqlite"
