from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statuses", "0002_alter_status_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="status",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]