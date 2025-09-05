from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from task_manager.mixins import (
    ContextDeleteMixin,
    ContextMixin,
    CustomLoginRequiredMixin,
)

from .forms import TaskFilter, TaskForm
from .models import Task


class TaskListView(CustomLoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/index.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter


class TaskCreateView(CustomLoginRequiredMixin, ContextMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks_index")
    text = _("Create task")
    button = _("Create")
    success_message = _("Task created successfully")
    error_message = _("Please correct the errors below.")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin, ContextMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks_index")
    text = _("Update task")
    button = _("Update")
    success_message = _("Task updated successfully")
    error_message = _("Please correct the errors below.")


class TaskDeleteView(
    CustomLoginRequiredMixin,
    UserPassesTestMixin,
    ContextDeleteMixin,
    DeleteView
):
    model = Task
    template_name = "general_delete_form.html"
    success_url = reverse_lazy("tasks_index")
    text = _("Delete task")
    success_delete_message = _("Task successfully deleted")

    def test_func(self):
        return self.request.user == self.get_object().owner

    def handle_no_permission(self):
        if not self.test_func():
            messages.error(
                self.request,
                _("A task can only be deleted by its author."))
            return redirect(self.success_url)
        messages.error(self.request, self.permission_denied_message)
        return super().handle_no_permission()


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_object()
        return context