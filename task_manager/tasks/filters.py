import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Labels
from task_manager.status.models import Statuses
from task_manager.tasks.models import Tasks
from django.contrib.auth import get_user_model


User = get_user_model()

class TaskFilter(django_filters.FilterSet):

    labels = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(),
        label=_('Labels'),
        widget=forms.Select(attrs={'class': 'form-select'}))

    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Author'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    users_tasks = django_filters.BooleanFilter(
        method='filter_users_tasks',
        label=_('Show only my tasks'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = Tasks
        fields = ['executor', 'status', 'labels', 'users_tasks']

    def filter_users_tasks(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.get('request')
