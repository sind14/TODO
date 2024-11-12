from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic


from .forms import TaskForm
from .models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "list/index.html"

    def get_queryset(self):
        return Task.objects.order_by("-datetime")


class TaskAddView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "list/add_task.html"
    success_url = reverse_lazy("list:index")


class TaskCompleteView(generic.View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.POST.get("action") == "Undo":
            task.is_completed = False
            task.save()
            return redirect(reverse("list:update_task", args=[task.pk]))
        task.is_completed = not task.is_completed
        task.save()
        return redirect("list:index")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "list/add_task.html"
    success_url = reverse_lazy("list:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "list/delete_form.html"
    success_url = reverse_lazy("list:index")


class TagsListView(generic.ListView):
    model = Tag
    context_object_name = "tags_list"
    template_name = "list/tags.html"
    success_url = reverse_lazy("list:tags")


class TagAddView(generic.CreateView):
    model = Tag
    fields = "__all__"
    template_name = "list/add_tag.html"
    success_url = reverse_lazy("list:tags")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    template_name = "list/add_tag.html"
    success_url = reverse_lazy("list:tags")


class TagDeleteView(generic.DeleteView):
    model = Tag
    template_name = "list/delete_form.html"
    success_url = reverse_lazy("list:tags")
