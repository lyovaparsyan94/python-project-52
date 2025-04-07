from django.forms import ModelForm
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Statuses
from django.core.exceptions import ValidationError


class StatusForm(ModelForm):

    class Meta:
        model = Statuses
        fields = [
            'name'
        ]