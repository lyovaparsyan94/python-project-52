from django.urls import reverse
from django.db import models
from django.utils import timezone
# Create your models here.

class Labels(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    
    def __str__(self):

        return self.name

    