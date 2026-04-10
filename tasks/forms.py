from django import forms
from django.contrib.auth.models import User
from .models import Task
import django_filters
from task_manager.models import Status, Label


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label='Исполнитель',
        empty_label='---------'
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].queryset = User.objects.all()
        self.fields['executor'].label_from_instance = (
            lambda user: f"{user.first_name} {user.last_name}".strip() or user.username
        )

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), 
        label='Статус', 
        empty_label='Все статусы'
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), 
        label='Исполнитель', 
        empty_label='Все исполнители'
    )
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(), 
        label='Метка'
    )
    
    is_owner = django_filters.BooleanFilter(
        method='filter_is_owner',
        label='Только свои задачи'
    )
    
    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'is_owner']

    def filter_is_owner(self, queryset, name, value):
        print(f"🔍 is_owner value: {value} | type: {type(value)}")
        print(f"🔍 request.user: {self.request.user}")
        if value:
            return queryset.filter(author=self.request.user)
        return queryset