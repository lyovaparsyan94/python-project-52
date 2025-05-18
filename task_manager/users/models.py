from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.username

    def __str__(self):
        return self.get_full_name()
