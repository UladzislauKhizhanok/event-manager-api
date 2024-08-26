from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="type",
            field=models.CharField(
                choices=[
                    ("conference", "Conference"),
                    ("workshop", "Workshop"),
                    ("meetup", "Meetup"),
                    ("webinar", "Webinar"),
                ],
                default="conference",
                max_length=50,
            ),
        ),
    ]
