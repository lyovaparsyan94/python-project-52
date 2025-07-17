from django.db import models
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label
# Create your models here.


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='author')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='executor')
    labels = models.ManyToManyField(Label, through='TaskLabelRelation', blank=True, related_name='labels')

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)