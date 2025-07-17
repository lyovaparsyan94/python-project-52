from django import forms

from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'autofocus': True,
                                    'class': 'form-control',
                                    'placeholder': 'Имя'})
    )