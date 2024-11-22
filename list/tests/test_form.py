from django.test import TestCase
from list.forms import TaskForm
from list.models import Task,Tag
from datetime import datetime, timedelta


class TaskFormTest(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")
        self.task1 = Task.objects.create(content="task1")
        self.task2 = Task.objects.create(content="task2")
        self.valid_data = {
            "content": "Task 1",
            "deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
            "tags": [self.tag1.id, self.tag2.id],
        }
        self.invalid_data = {
            "content": "Task 1",
            "deadline": "SEPTEMBER 22,year 2024",
            "tags": [self.tag2.id],
        }

    def test_task_form_valid(self):
        form = TaskForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), "Task form should be valid with correct data")

    def test_task_form_invalid(self):
        form = TaskForm(data=self.invalid_data)
        self.assertFalse(form.is_valid(), "Form should be invalid with incorrect data")

    def test_task_form_creation(self):
        self.assertEqual(Task.objects.count(), 2, "Should be 2 tasks in the database")
