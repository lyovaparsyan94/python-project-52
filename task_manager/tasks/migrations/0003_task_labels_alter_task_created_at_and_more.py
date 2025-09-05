import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0001_initial"),
        ("statuses", "0004_alter_status_options_alter_status_created_at_and_more"),
        ("tasks", "0002_alter_task_name_alter_task_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(
                related_name="tasks_labels", to="labels.label", verbose_name="Labels"
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(verbose_name="Description"),
        ),
        migrations.AlterField(
            model_name="task",
            name="executor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tasks_executed",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Executor",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="name",
            field=models.CharField(max_length=150, unique=True, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="task",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tasks_owned",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Owner",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tasks",
                to="statuses.status",
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
    ]