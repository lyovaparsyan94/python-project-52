import django_filters
from django.forms.widgets import CheckboxInput
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    user_tasks = django_filters.BooleanFilter(
        label=_("Only my own tasks"),
        method="filter_user_tasks",
        widget=CheckboxInput,
    )
    labels = django_filters.ModelChoiceFilter(
        label=_("Label"),
        queryset=Label.objects.all(),
    )

    def filter_user_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "executor", "labels"]
