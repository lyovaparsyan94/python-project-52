import django_filters
from django import forms

from .models import Label, Status, Task, User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label='Статус',
        queryset=Status.objects.all() 
    )
    
    executor = django_filters.ModelChoiceFilter(
        label='Исполнитель',
        queryset=User.objects.all()
    )
    
    labels = django_filters.ModelChoiceFilter(
        label='Метка',
        queryset=Label.objects.all() 
    )

    my_tasks = django_filters.BooleanFilter(
        label='Только свои задачи',
        method='filter_my_tasks',
        widget=forms.CheckboxInput,
    )

    def filter_my_tasks(self, queryset, name, value):
        if value: 
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'executor': ['exact'],
            'labels': ['exact']
        }
