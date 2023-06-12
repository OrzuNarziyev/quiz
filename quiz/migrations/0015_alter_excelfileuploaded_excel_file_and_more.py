# Generated by Django 4.1.7 on 2023-06-01 18:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("quiz", "0014_excelfileuploaded_alter_question_uuid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="excelfileuploaded",
            name="excel_file",
            field=models.FileField(upload_to="excel", verbose_name="Excel File"),
        ),
        migrations.AlterField(
            model_name="question",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("a20d9611-0620-461c-8a7d-4daf7098dd05"),
                editable=False,
                unique=True,
            ),
        ),
    ]
