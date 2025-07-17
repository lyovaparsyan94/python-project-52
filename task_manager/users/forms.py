from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance.pk:  # Режим редактирования
            if User.objects.filter(username=username).exclude(
                    pk=self.instance.pk).exists():
                raise ValidationError(
                    "Пользователь с таким именем уже существует.")
        else:  # Режим создания
            if User.objects.filter(username=username).exists():
                raise ValidationError(
                    "Пользователь с таким именем уже существует.")
        return username


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
