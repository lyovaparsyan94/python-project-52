import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0002_alter_status_name"),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tasks",
                to="statuses.status",
            ),
        ),
    ]