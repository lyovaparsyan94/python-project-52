# Generated by Django 5.1.4 on 2025-01-20 20:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_rename_performer_task_executor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Executor', to=settings.AUTH_USER_MODEL, verbose_name='Executor'),
        ),
    ]
