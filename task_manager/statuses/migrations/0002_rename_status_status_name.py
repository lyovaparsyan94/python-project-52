# Generated by Django 5.1.4 on 2025-01-20 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='status',
            new_name='name',
        ),
    ]
