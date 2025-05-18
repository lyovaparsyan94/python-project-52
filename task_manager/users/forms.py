from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")


class Create(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]


class Update(Create):

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (
            username
            and (self._meta.model.objects
            .filter(username__iexact=username).exists())
            and self.instance.username != username
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username
