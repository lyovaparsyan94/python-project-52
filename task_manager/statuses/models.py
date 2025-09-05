from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        max_length=100, null=False, unique=True, verbose_name=_("Name")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Task status")
        verbose_name_plural = _("Task statuses")

    def __str__(self) -> str:
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.tasks.exists():
            related_objects = self.tasks.all()
            raise models.ProtectedError(
                _("Can't delete status because it's in use"), related_objects
            )
        return super().delete(using, keep_parents)