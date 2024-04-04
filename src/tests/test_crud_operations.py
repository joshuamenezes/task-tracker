import unittest
from ..util.db import TaskDAO
from datetime import datetime
from ..util.constants import TEST_DB_NAME
from ..init_db import *
import sqlite3


class TestCRUDBasic(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dao = TaskDAO()
        create_db(TEST_DB_NAME)

    @classmethod
    def tearDownClass(cls) -> None:
        delete_db(TEST_DB_NAME)

    def test_WhenTaskIsCreated_It_ShouldAppearInTheDatabase(self):
        task1 = [
            "Test task",
            "Description",
            datetime.strptime(
                datetime.today(),
                '%m/%d/%y').strftime('%Y-%m-%d'),
            1,
            "TestTag"]

        task_id = self.dao.create_task(*task1)
        self.assertNotEqual(task_id, [], "Task not created")

        res = self.dao.get_task(task_id)
        self.assertNotEqual(
            res, [], f"No task with id {task_id} exists in the database")

    def test_WhenTaskIsDeleted_It_ShouldUpdateTheDatabase(self):
        task2 = [
            "Test task 2",
            "Description",
            datetime.strptime(
                datetime.today(),
                '%m/%d/%y').strftime('%Y-%m-%d'),
            1,
            "TestTag"]

        task_id = self.dao.create_task(*task2)
        self.assertNotEqual(task_id, None, "Task not created")

        rows_deleted = self.dao.delete_task(task_id)
        self.assertEqual(1, rows_deleted)

        # Sanity check
        empty_task = self.dao.get_task(task_id)
        self.assertEqual([], empty_task)

    def test_WhenTaskIsUpdated_It_ShouldUpdateTheDatabase(self):
        task3 = [
            "Test task 3",
            "Description",
            datetime.strptime(
                datetime.today(),
                '%m/%d/%y').strftime('%Y-%m-%d'),
            1,
            "TestTag"]

        task_id = self.dao.create_task(*task3)

        rows_updated = self.dao.update_task(
            task_id, description="Updated description")
        self.assertEqual(1, rows_updated)

    def test_WhenMultipleTasksExist_It_ShouldRetrieveASpecificOne(self):
        task4 = [
            "Test task 4",
            "Description",
            datetime.strptime(
                datetime.today(),
                '%m/%d/%y').strftime('%Y-%m-%d'),
            1,
            "TestTag"]
        task5 = [
            "Test task 5",
            "Description",
            datetime.strptime(
                datetime.today(),
                '%m/%d/%y').strftime('%Y-%m-%d'),
            1,
            "TestTag"]
        task6 = [
            "Test task 6",
            "Description",
            datetime.strptime(
                datetime.today(),
                '%m/%d/%y').strftime('%Y-%m-%d'),
            1,
            "TestTag"]

        task_id4 = self.dao.create_task(*task4)
        task_id5 = self.dao.create_task(*task5)
        task_id6 = self.dao.create_task(*task6)

        task = self.dao.get_task(task6)
        self.assertNotEqual(task, [])


if __name__ == '__main__':
    unittest.main()
