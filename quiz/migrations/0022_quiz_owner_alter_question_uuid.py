# Generated by Django 4.1.7 on 2023-07-11 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quiz", "0021_quiz_period_date_alter_question_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("73826c85-670e-469f-b8a0-1b02e1eacfc2"),
                editable=False,
                unique=True,
            ),
        ),
    ]
