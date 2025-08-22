from django.forms import ModelForm

from task_manager.mixins import FormStyleMixin
from task_manager.tasks.models import Task


class TaskCreationForm(FormStyleMixin, ModelForm):
    """
    Form for creating or updating tasks with labels, status, and executor.
    """
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
