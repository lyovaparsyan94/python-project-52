from django.db import models


# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='именем')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'labels'
        verbose_name = 'Метки'
        verbose_name_plural = 'Меток'
    
    def __str__(self):
        return self.name
