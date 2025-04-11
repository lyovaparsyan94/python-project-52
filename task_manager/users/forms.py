from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    SetPasswordMixin,
)
from django.contrib.auth.forms import (
    UserChangeForm as DjangoUserChangeForm,
)
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
)


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
        ) + DjangoUserCreationForm.Meta.fields


class UserChangeForm(SetPasswordMixin, DjangoUserChangeForm):
    password = None
    password1, password2 = SetPasswordMixin.create_password_fields()

    class Meta(DjangoUserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
