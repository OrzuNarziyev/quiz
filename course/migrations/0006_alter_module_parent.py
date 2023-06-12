# Generated by Django 4.1.7 on 2023-06-05 10:37

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0005_alter_course_subject"),
    ]

    operations = [
        migrations.AlterField(
            model_name="module",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="course.module",
                verbose_name="Bo'lim",
            ),
        ),
    ]
