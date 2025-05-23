# Generated by Django 5.2 on 2025-05-18 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_alter_labels_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(error_messages={'unique': 'This label with this name already exists. Please choose another name.'}, max_length=255, unique=True, verbose_name='Name'),
        ),
    ]
