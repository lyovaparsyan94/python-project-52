from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


def debug_lang(request):
    from django.utils import translation
    info = {
        "REQUEST_LANGUAGE": request.LANGUAGE_CODE,
        "GET_LANGUAGE": translation.get_language(),
        "SESSION_LANGUAGE": request.session.get('django_language', 'not set'),
        "COOKIE_LANGUAGE": request.COOKIES.get('django_language', 'not set'),
        "LOCALE_PATHS": settings.LOCALE_PATHS,
    }
    return render(request, 'debug.html', {'info': info})


def index(request):
    return render(request, 'index.html')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно создана")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        return response


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно изменена")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        return response


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно удалена")

    def test_func(self):
        return self.request.user == self.get_object().creator


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs
