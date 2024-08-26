import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("capacity", models.IntegerField()),
                (
                    "attendees",
                    models.ManyToManyField(blank=True, related_name="events_attending", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
