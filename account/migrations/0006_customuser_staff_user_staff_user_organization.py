# Generated by Django 4.1.7 on 2023-06-24 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_customuser_organizations"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="staff_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to="account.staff_user",
            ),
        ),
        migrations.AddField(
            model_name="staff_user",
            name="organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="staff_user",
                to="account.organizations",
            ),
        ),
    ]
