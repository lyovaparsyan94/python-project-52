from django.db import models

from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание", blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name="tasks_created")
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="tasks_assigned",
        null=True, blank=True)
    labels = models.ManyToManyField(
        'labels.Label', blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
