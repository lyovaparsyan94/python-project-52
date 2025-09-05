from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last name"))
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Username")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def delete(self, *args, **kwargs):
        protected_tasks = self.tasks_owned.all() | self.tasks_executed.all()

        if protected_tasks.exists():
            raise models.ProtectedError(
                "User cannot be deleted because it is in use.",
                protected_tasks
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
