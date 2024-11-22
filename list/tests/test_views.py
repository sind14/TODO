from django.test import TestCase
from django.urls import reverse

from list.models import Task, Tag

TASK_LIST_URL = reverse("list:index")
TAG_LIST_URL = reverse("list:tags")


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")
        self.task1 = Task.objects.create(content="Task1")
        self.task2 = Task.objects.create(content="Task2")
        self.task3 = Task.objects.create(content="Task3")

    def get_task_list_response(self):
        return self.client.get(TASK_LIST_URL)

    def get_tag_list_response(self):
        return self.client.get(TAG_LIST_URL)


class TaskListViewTest(BaseTest):
    def test_create_task(self) -> None:
        self.assertEqual(self.get_task_list_response().status_code, 200)
        tasks_in_order = Task.objects.order_by("-datetime")
        self.assertEqual(
            list(self.get_task_list_response().context["task_list"]),
            list(tasks_in_order),
        )
        self.assertTemplateUsed(self.get_task_list_response(), "list/index.html")

    def test_delete_task(self) -> None:
        Task.objects.filter(content="Task1").delete()
        self.assertEqual(self.get_task_list_response().status_code, 200)
        tasks_in_order = Task.objects.order_by("-datetime")
        self.assertEqual(
            list(self.get_task_list_response().context["task_list"]),
            list(tasks_in_order),
        )
        self.assertTemplateUsed(self.get_task_list_response(), "list/index.html")

    def test_task_ordering(self) -> None:
        self.assertEqual(self.get_task_list_response().status_code, 200)
        tasks_in_order = Task.objects.order_by("-datetime")
        self.assertEqual(
            list(self.get_task_list_response().context["task_list"]),
            list(tasks_in_order),
        )
        self.assertTemplateUsed(self.get_task_list_response(), "list/index.html")

    def test_mark_task_complete(self) -> None:
        self.assertFalse(self.task1.is_completed)
        res = self.client.post(reverse("list:complete_task", args=[self.task1.pk]))
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)
        self.assertRedirects(res, reverse("list:index"))

    def test_mark_task_undo(self) -> None:
        self.task2.is_completed = True
        self.task2.save()
        self.assertTrue(self.task2.is_completed)
        res = self.client.post(reverse("list:complete_task", args=[self.task2.pk]), {"action": "Undo"})
        self.task2.refresh_from_db()
        self.assertFalse(self.task2.is_completed)
        self.assertRedirects(res, reverse("list:update_task", args=[self.task2.pk]))


class TagListViewTest(BaseTest):
    def test_create_tag(self) -> None:
        self.assertEqual(self.get_tag_list_response().status_code, 200)
        self.assertEqual(
            list(self.get_tag_list_response().context["tags_list"]),
            list(Tag.objects.all()),
        )
        self.assertTemplateUsed(self.get_tag_list_response(), "list/tags.html")

    def test_delete_tag(self) -> None:
        Tag.objects.filter(name="Tag1").delete()
        self.assertEqual(self.get_tag_list_response().status_code, 200)
        self.assertEqual(
            list(self.get_tag_list_response().context["tags_list"]),
            list(Tag.objects.all()),
        )
        self.assertTemplateUsed(self.get_tag_list_response(), "list/tags.html")
