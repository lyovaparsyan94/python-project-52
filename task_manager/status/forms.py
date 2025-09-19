from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Statuses


class CreateStatusForm(forms.ModelForm):

    name = forms.CharField(
        label=_('Name status'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Name status')
        })
    )

    class Meta:
        model = Statuses
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if Statuses.objects.filter(name__iexact=name).exists():
            raise ValidationError(_('This name is already taken'))

        return name


class UpdateStatusForm(CreateStatusForm):
    pass
