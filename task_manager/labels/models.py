from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

# Create your models here.


class Labels(models.Model):
    name = models.CharField(gettext_lazy("Name"), max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.name
