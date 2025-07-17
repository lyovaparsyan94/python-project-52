from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Именем')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='task_creator',
        verbose_name='Автор',
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='task_executor',
        verbose_name='Исполнитель',
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='task_status',
        verbose_name='Статус',
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name='Метки',
        related_name='task_label',
        blank=True,
    )

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'