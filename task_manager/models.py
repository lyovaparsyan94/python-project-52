from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Status(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name=_('Имя'))

    class Meta:
        verbose_name = _('Статус')
        verbose_name_plural = _('Статусы')

    def __str__(self):
        return self.name

    def clean(self):
        if self.pk is None and Status.objects.filter(name=self.name).exists():
            raise ValidationError({'name': _('уже существует')})
        
class Label(models.Model):
    name = models.CharField(
        verbose_name=_('имя'),
        max_length=255,
        unique=True,
        help_text=_('Уникальное название метки'),
    )
    created_at = models.DateTimeField(
        verbose_name=_('дата создания'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('метка')
        verbose_name_plural = _('метки')
        ordering = ['name']

    def __str__(self):
        return self.name
        
