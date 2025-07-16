from django.db import models


# Create your models here.
class Labels(models.Model):
    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name