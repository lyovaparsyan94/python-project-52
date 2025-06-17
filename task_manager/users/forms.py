from django.contrib.auth.forms import UserCreationForm
from .models import User


class TaskManagerUserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].label = 'Имя'
        self.fields['first_name'].max_length = 150
        self.fields['first_name'].required = True

        self.fields['last_name'].label = 'Фамилия'
        self.fields['last_name'].max_length = 150
        self.fields['last_name'].required = True

        self.fields['username'].label = 'Имя пользователя'
        self.fields['username'].max_length = 150
        self.fields['username'].required = True
        self.fields['username'].help_text = 'Обязательное поле. \
            Не более 150 символов. Только буквы, \
                цифры и символы @/./+/-/_.'

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = """
            <ul>
                <li>Ваш пароль должен содержать как минимум 3 символа.</li>
            </ul>
        """
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].help_text = "Для подтверждения введите, \
            пожалуйста, пароль ещё раз."


class UpdateUser(TaskManagerUserCreateForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username
