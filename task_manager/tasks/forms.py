from django.forms import ModelForm

from .consts import TasksConst
from .models import Label, Status, Task


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': TasksConst.frm_label_name,
        }
        error_messages = {
            'name': {
                'max_length': TasksConst.frm_name_too_long,
                'required': TasksConst.frm_required_field,
                'unique': TasksConst.frm_uniq_status
            },
        }


class StatusFormDelete(ModelForm):
    class Meta:
        model = Status
        fields = []
        labels = {}


class LabelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name':  TasksConst.frm_label_name,
        }
        error_messages = {
            'name': {
                'max_length': TasksConst.frm_name_too_long,
                'required': TasksConst.frm_required_field,
                'unique': TasksConst.frm_uniq_label
            },
        }


class LabelFormDelete(ModelForm):
    class Meta:
        model = Label
        fields = []
        labels = {}


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': TasksConst.frm_label_name,
            'description': TasksConst.frm_label_descr, 
            'status': TasksConst.frm_label_status, 
            'executor': TasksConst.frm_label_assigned_to,
            'labels': TasksConst.labels_terms
        }
        error_messages = {
            'name': {
                'max_length': TasksConst.frm_name_too_long,
                'required': TasksConst.frm_required_field,
                'unique': TasksConst.frm_unic_task
            },
        }


class TaskFormDelete(ModelForm):
    class Meta:
        model = Label
        fields = []
        labels = {}
