from django import forms

from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        
    name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'autofocus': True,
                                    'class': 'form-control',
                                    'placeholder': 'Имя'})
    )