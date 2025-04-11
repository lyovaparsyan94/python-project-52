from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.mixins import AuthorAccessOnlyMixin, LoginRequiredMixin
from task_manager.tasks.filter import TaskFilter
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"
    ordering = ["id"]
    extra_context = {
        "title": _("Tasks"),
        "create": _("Create task"),
        "find": _("Filter"),
        "edit": _("Edit"),
        "delete": _("Delete"),
    }


class TaskInfoView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_info.html"
    context_object_name = "task"
    extra_context = {
        "title": _("Task"),
        "author": _("Author"),
        "performer": _("Performer"),
        "status": _("Status"),
        "createdate": _("Creation date"),
        "update": _("Last update"),
        "labels": _("Labels"),
        "edit": _("Edit"),
        "delete": _("Delete"),
    }


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = "form.html"
    form_class = TaskCreationForm
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task was created successfully")
    extra_context = {"title": _("Create task"), "button_name": _("Create")}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = "form.html"
    form_class = TaskCreationForm
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task was updated successfully")
    extra_context = {"title": _("Update task"), "button_name": _("Update")}


class TaskDeleteView(
    LoginRequiredMixin,
    AuthorAccessOnlyMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("Task was deleted successfully")
    permission_denied_url = reverse_lazy("tasks_list")
    permission_denied_message = _("Only the task's author can delete it")
    extra_context = {
        "title": _("Delete task"),
        "button_name": _("Yes, delete"),
        "question": _("Are you sure you want to delete"),
    }
