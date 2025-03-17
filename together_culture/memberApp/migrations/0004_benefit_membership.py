# Generated by Django 5.1.6 on 2025-03-08 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loginRegistrationApp", "0004_alter_events_labels_alter_events_tags"),
        (
            "memberApp",
            "0003_digitalcontentmodule_remove_booking_digital_module_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Benefit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("max_usage", models.PositiveIntegerField()),
                ("used_count", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("active", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="loginRegistrationApp.users",
                    ),
                ),
            ],
        ),
    ]
