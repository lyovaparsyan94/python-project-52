from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Labels
from task_manager.status.models import Statuses
from task_manager.tasks.models import Tasks
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateTaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['labels'].required = False

    status = forms.ModelChoiceField(
        queryset=Statuses.objects.all(),
        label=_('Status'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Executor'),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Labels.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select form-select-sm'
        }),
        label=_('Labels')
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if hasattr(self, 'instance') and self.instance.pk:
            if Tasks.objects.filter(name=name).exclude(
                    pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    _("Task with this name already exists."))
        else:
            if Tasks.objects.filter(name=name).exists():
                raise forms.ValidationError(
                    _("Task with this name already exists."))

        return name

    class Meta:
        model = Tasks
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            'name': _('Name'),
            'description': _('Description'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': _('Name'),
                'class': 'form-control'
                }
            ),
            'description': forms.Textarea(attrs={
                'placeholder': _('Description'),
                'class': 'form-control'
                }
            ),
        }


class UpdateTaskForm(CreateTaskForm):
    pass
