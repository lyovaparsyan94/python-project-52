from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )

    def __str__(self):
        full_name = self.first_name + ' ' + self.last_name
        return full_name
