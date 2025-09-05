from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Name"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"))

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        related_tasks = self.tasks_labels.all()
        if related_tasks.exists():
            raise models.ProtectedError(
                _("Label is in use and cannot be deleted."), related_tasks
            )
        super().delete(*args, **kwargs)