from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import MessageMixin

from .filters import TaskFilter
from .forms import CreateTaskForm, UpdateTaskForm
from .models import Tasks


class TasksView(LoginRequiredMixin, FilterView):
    model = Tasks
    template_name = 'task_template/tasks.html'
    context_object_name = 'tasks'
    login_url = '/login/'
    filterset_class = TaskFilter


class TaskUpdate(LoginRequiredMixin, MessageMixin, UpdateView):
    model = Tasks
    template_name = 'task_template/task_update.html'
    context_object_name = 'update_task'
    login_url = '/login/'
    form_class = UpdateTaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task updated successfully')
    error_message = _('Task with this Name already exists')

    def get_context_data(self, **kwargs):
        task = self.object
        context = super().get_context_data(**kwargs)
        context['button_text'] = _("Update")
        context['task_id'] = task.id
        context['title_text'] = _('Update task')
        return context


class TaskCreate(LoginRequiredMixin, MessageMixin, CreateView):
    model = Tasks
    template_name = 'task_template/task_create.html'
    context_object_name = 'create_task'
    login_url = '/login/'
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task created successfully')
    error_message = _('Task with this Name already exists')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _("Create")
        context['title_text'] = _("Create Task")
        return context


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tasks
    template_name = 'task_template/task_delete.html'
    success_url = reverse_lazy('tasks')
    login_url = '/login/'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('A task can only be deleted by its author'))
        return redirect('tasks')

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        messages.success(request, _('Task deleted successfully!'))
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.get_object()
        return context


class TaskView(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'task_template/task.html'
    context_object_name = 'task'
    login_url = 'login/'

    def get_queryset(self):
        return Tasks.objects.prefetch_related('labels')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = self.object.labels.all()
        return context
