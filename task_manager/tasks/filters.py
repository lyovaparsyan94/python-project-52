import django_filters
from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User

from .models import Task


class TaskFilter(django_filters.FilterSet):

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label="Статус"
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Исполнитель'
    )

    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка'
    )

    my_tasks = django_filters.BooleanFilter(
        method='filter_my_tasks',
        widget=forms.CheckboxInput,
        label="Только свои задачи"
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']
        labels = {
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метка'
        }

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
