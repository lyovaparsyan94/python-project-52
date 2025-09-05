from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0003_alter_status_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Task status', 'verbose_name_plural': 'Task statuses'},
        ),
        migrations.AlterField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='status',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]