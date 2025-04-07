from django.forms import ModelForm
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Tasks
from django.core.exceptions import ValidationError


class TasksForm(ModelForm):

    class Meta:
        model = Tasks
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'label'
        ]