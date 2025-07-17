from django.shortcuts import render, redirect
from django.views import View
from task_manager.tasks.models import Task
from task_manager.tasks.forms import CreateTaskForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .filters import TaskFilter
from django.views.generic import DetailView
from task_manager.users.models import User


class TasksView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = CreateTaskForm()
        return render(request, 'tasks/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = User.objects.get(pk=request.user.id)
            task.save()
            messages.success(request, _('Task successfully created'))
            return redirect('tasks')
        return render(request, 'tasks/create.html', {'form': form})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _("Task successfully changed")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, self.success_message)
        return redirect('tasks')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/delete.html'
    success_message = _("Task successfully deleted")

    def form_valid(self, form):
        if self.object.author.id == self.request.user.id:
            messages.success(self.request, self.success_message)
            return super().form_valid(form)
        messages.error(self.request, _("A task can only be deleted by its author"))
        return redirect('tasks')


class TaskShowView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'