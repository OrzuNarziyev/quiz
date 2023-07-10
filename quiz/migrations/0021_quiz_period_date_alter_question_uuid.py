# Generated by Django 4.1.7 on 2023-07-05 03:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0020_alter_question_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="period_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="question",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("12fe6d5d-199b-4036-a433-44b2cd78a701"),
                editable=False,
                unique=True,
            ),
        ),
    ]
