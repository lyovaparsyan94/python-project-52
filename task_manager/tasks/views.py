from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.tasks.filters import TaskFilter

# from .forms import CreateUserForm
from .forms import (
    CreateTaskForm,
)
from .models import Task


class BaseTaskView(LoginRequiredMixin, View):
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please sign in.'))
        return super().dispatch(request, *args, **kwargs)


class IndexTaskView(BaseTaskView):    
    def get(self, request):
        tasks = Task.objects.all()
        filterset = TaskFilter(request.GET, queryset=tasks, request=request)
        return render(
            request,
            'tasks/index.html',
            context={
                'form': filterset.form,
                'tasks': filterset.qs,
            }
        )
    

class CreateTaskView(BaseTaskView):
    def get(self, request):
        form = CreateTaskForm()
        return self._render_form(request, form)
    
    def post(self, request):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, _('Task successfully created'))
            return redirect('tasks')
        return self._render_form(request, form)
    
    def _render_form(self, request, form):
        return render(
            request,
            'tasks/create.html',
            context={
                'form': form
            }
        )


class ViewTaskView(BaseTaskView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(
            request,
            'tasks/view.html',
            context={
                'task': task
            }
        )


class UpdateTaskView(BaseTaskView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = CreateTaskForm(instance=task)
        return render(
            request,
            'tasks/update.html',
            context={
                'form': form,
                'task': task
            }
        )

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task successfully updated'))
            return redirect('tasks')
        return render(
            request,
            'tasks/update.html',
            context={
                'form': form,
                'task': task
            }
        )


class DeleteTaskView(BaseTaskView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(
            request,
            'tasks/delete.html',
            context={
                'task': task
            }
        )
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.author != request.user:
            messages.error(request, _('Only the author can delete the task'))
            return redirect('tasks')
        task.delete()
        messages.success(request, _('Task successfully deleted'))
        return redirect('tasks')