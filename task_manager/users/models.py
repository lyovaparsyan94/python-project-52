from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(
        blank=False, max_length=50, verbose_name=_("First Name")
    )
    last_name = models.CharField(
        blank=False, max_length=50, verbose_name=_("Last Name")
    )
    username = models.CharField(
        blank=False, max_length=50, verbose_name=_("Username"), unique=True
    )

    USERNAME_FIELD = "username"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
