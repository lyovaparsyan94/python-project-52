from django.urls import reverse
from django.db import models
from django.utils import timezone
from task_manager.statuses.models import Statuses
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from task_manager.labels.models import Labels
# Create your models here.

class Tasks(models.Model):
    name = models.CharField(gettext_lazy('name'), max_length=255, unique=True)
    status = models.ForeignKey(Statuses, related_name='status', blank=False, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='creator')
    executor = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='executor', null=True, blank=True)
    description = models.TextField(gettext_lazy('description'), blank=True)
    label = models.ManyToManyField(Labels, through='LabelsTasksReal', related_name='label', blank=True)


    def __str__(self):

        return self.name

class LabelsTasksReal(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.CASCADE)
    