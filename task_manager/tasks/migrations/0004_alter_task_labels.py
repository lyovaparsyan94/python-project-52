from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0001_initial"),
        ("tasks", "0003_task_labels_alter_task_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(
                blank=True,
                related_name="tasks_labels",
                to="labels.label",
                verbose_name="Labels",
            ),
        ),
    ]