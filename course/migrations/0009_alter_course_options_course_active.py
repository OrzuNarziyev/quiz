# Generated by Django 5.0.2 on 2024-02-12 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_alter_course_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='course',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Фаоллаштириш'),
        ),
    ]
