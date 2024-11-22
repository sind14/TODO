from django.urls import path
from list.views import (
    TaskListView,
    TaskAddView,
    TaskCompleteView,
    TaskUpdateView,
    TaskDeleteView,
    TagsListView,
    TagAddView,
    TagUpdateView,
    TagDeleteView,
)

app_name = "list"

urlpatterns = [
    path("", TaskListView.as_view(), name="index"),
    path("add_task", TaskAddView.as_view(), name="add_task"),
    path("complete_task/<int:pk>", TaskCompleteView.as_view(), name="complete_task"),
    path("update_task/<int:pk>", TaskUpdateView.as_view(), name="update_task"),
    path("delete_task/<int:pk>", TaskDeleteView.as_view(), name="delete_task"),
    path("tags", TagsListView.as_view(), name="tags"),
    path("tags/add_tag", TagAddView.as_view(), name="add_tag"),
    path("update_tag/<int:pk>", TagUpdateView.as_view(), name="update_tag"),
    path("delete_tag/<int:pk>", TagDeleteView.as_view(), name="delete_tag"),
]
