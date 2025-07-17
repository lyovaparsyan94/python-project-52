from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import View

from .forms import TaskFilterForm, TaskForm
from .models import Task


# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
        status = request.GET.get('status')
        executor = request.GET.get('executor')
        labels = request.GET.get('labels')
        own_task = request.GET.get('own_task')
        tasks = Task.objects.all()
        if status:
            tasks = tasks.filter(status_id=status)
        if executor:
            tasks = tasks.filter(executor_id=executor)
        if labels:
            tasks = tasks.filter(labels=labels)
        if own_task == 'on':
            tasks = tasks.filter(creator=request.user)
        form = TaskFilterForm(request.GET)
        return render(
            request,
            'tasks/index.html',
            {'form': form,
             'tasks': tasks, }
        )
    
    
class TaskView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        return render(
            request,
            'tasks/task.html',
            {'task': task}
        )

    
class TaskCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
        form = TaskForm()
        return render(
            request,
            'tasks/create.html',
            {'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Задача успешно создана')
            return redirect(reverse('all_tasks'))
        return render(
            request,
            'tasks/create.html',
            {'form': form}
        )
    
    
class TaskUpdateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        form = TaskForm(instance=task)
        return render(
            request,
            'tasks/update.html',
            {'form': form,
             'task_id': task_id}
        )
        
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = Task.objects.get(id=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Задача успешно изменена')
            return redirect(reverse('all_tasks'))
        return render(
            request, "tasks/update.html", {"form": form,
                                              "task_id": task_id}
        )
    
    
class TaskDeleteView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                            'Вы не авторизованы! Пожалуйста, выполните вход.')
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        if request.user != task.creator:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Задачу может удалить только ее автор')
            return redirect(reverse('all_tasks'))
        return render(
            request,
            'tasks/delete.html',
            {'task_id': task_id,
             'task': task}
        )
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = Task.objects.get(id=task_id)
        if request.user != task.creator:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Задачу может удалить только ее автор')
            return redirect(reverse('all_tasks'))
        task.delete()
        messages.add_message(request,
                                 messages.SUCCESS,
                                 'Задача успешно удалена')
        return redirect(reverse('all_tasks'))
    