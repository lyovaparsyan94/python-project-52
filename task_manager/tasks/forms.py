from django import forms

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label='Статус',
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select',
            }
        )
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Исполнитель',
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select',
            }
        )
    )
    own_task = forms.BooleanField(
        required=False,
        label='Статус',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )
    labels = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label='Метка',
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select',
            }
        )
    )
    
    
class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'autofocus': True,
            }
        )
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            }
        )
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label='Статус',
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select',
            }
        )
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Исполнитель',
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-select',
            }
        )
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        label='Метки',
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
            }
        )
    )
    
    class Meta:
        model = Task
        fields = ('name', 'description', 'labels', 'status', 'executor',)