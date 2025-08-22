from django.forms import ModelForm

from task_manager.mixins import FormStyleMixin
from task_manager.statuses.models import Status


class StatusCreationForm(FormStyleMixin, ModelForm):
    """Form for creating or updating a Status."""
    class Meta:
        model = Status
        fields = ['name']
