from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Statuses


class CreateStatusesForm(forms.ModelForm):

    class Meta:
        model = Statuses
        fields = [
            'name',
        ]
        labels = {
            'name': _('Name'),
        }

    def clean_name(self):
        status_name = self.cleaned_data['name']
        stasus = Statuses.objects.filter(name=status_name)

        if stasus.exists() and self.instance.pk != stasus[0].pk:
            raise forms.ValidationError(
                _('Task status with this Name already exists.')
            )
        return self.cleaned_data['name']