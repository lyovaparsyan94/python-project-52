# from django.contrib.auth.models import User


# class UserProxy(User):
#     class Meta:
#         proxy = True

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        max_length=150,
        blank=False
    )
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
