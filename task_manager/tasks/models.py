from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               verbose_name=_("Статус"))
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='created_tasks',
                                verbose_name=_("Автор"))
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_("Исполнитель")
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_("Дата создания"))
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        verbose_name=_("Метки")
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
