from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from task_manager.tasks.forms import TasksForm
from task_manager.mixins import AuthRequired
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.tasks.models import Tasks
from task_manager.tasks.mixins import CheckUser, NoPermissionHandleMixin
from task_manager.tasks.filter import TaskFilter
from django_filters.views import FilterView


class TasksListView(AuthRequired, FilterView):
    success_url = reverse_lazy('tasks:list')
    model = Tasks
    template_name = 'tasks/list.html'
    filterset_class = TaskFilter
    

class TasksCreate(AuthRequired, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = TasksForm   
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:list')
    success_message = gettext('Task create successfull')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class TasksUpdate(AuthRequired, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TasksForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:list')
    success_message = gettext('Task update successfull')


class TasksDelete(AuthRequired, NoPermissionHandleMixin, CheckUser, SuccessMessageMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = gettext('Task delete successfull')