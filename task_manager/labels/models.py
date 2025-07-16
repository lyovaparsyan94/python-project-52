from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name=_("Название"))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Дата создания"))
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_labels',
        verbose_name=_("Автор")
    )

    def __str__(self):
        return self.name
