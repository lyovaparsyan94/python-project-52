from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='именем')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'statuses'
        verbose_name = 'Статуса'
        verbose_name_plural = 'Статусы'
    
    def __str__(self):
        return self.name
