from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Labels
from task_manager.status.models import Statuses



class Tasks(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(_("description"), max_length=1000)
    status = models.ForeignKey(
        Statuses,
        related_name='sts',
        null=False,
        on_delete=models.PROTECT)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='task_author',
        null=False,
        on_delete=models.PROTECT)
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='task_maker',
        null=False,
        on_delete=models.PROTECT)
    labels = models.ManyToManyField(
        Labels, verbose_name=_("labels"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
