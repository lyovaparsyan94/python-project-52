from django_filters import FilterSet, CharFilter
from task_manager.tasks.models import Tasks
import django_filters
from task_manager.statuses.models import Statuses
from django.contrib.auth import get_user_model
from task_manager.labels.models import Labels
from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter



class TaskFilter(FilterSet):
    own_tasks = BooleanFilter(
        widget=forms.CheckboxInput(),
        field_name="creator",
        method="filter_own_tasks",
        label=_("Only own tasks"),
    )

    task_label = ModelChoiceFilter(
        queryset=Labels.objects.all(),
        field_name="labels",
        label=_("Label"),
    )

    class Meta:
        model = Tasks
        fields = ["status", "executor", "task_label", "own_tasks"]

    def filter_own_tasks(self, queryset, name, value):
        return queryset.filter(creator=self.request.user) if value else queryset