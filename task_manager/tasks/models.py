from django.db import models

from ..users.models import User


class TaskBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        abstract = True


class Status(TaskBaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)


class Label(TaskBaseModel):
    name = models.CharField(max_length=100, null=False, unique=True)


class Task(TaskBaseModel):
    name = models.CharField(max_length=250, null=False, unique=True)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_created'
        )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_executed',
        null=True,
        blank=True
        )
    labels = models.ManyToManyField(Label, blank=True)
