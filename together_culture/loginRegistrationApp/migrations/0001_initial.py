# Generated by Django 4.2.19 on 2025-02-19 10:21

#Migrations can be updated after models changes. See how to do it below:
#https://hernandis.me/2023/02/27/update-migrations-while-you-work-on-django-models.html

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Events",
            fields=[
                ("eventId", models.AutoField(primary_key=True, serialize=False)),
                ("eventName", models.CharField(max_length=100)),
                ("eventDate", models.DateTimeField()),
                ("startTime", models.TimeField()),
                ("endTime", models.TimeField()),
                ("location", models.CharField(max_length=100)),
                ("numberOfAttenders", models.IntegerField(auto_created=0)),
                ("shortDescription", models.CharField(max_length=50)),
                ("longDescription", models.CharField(max_length=500)),
                (
                    "eventType",
                    models.CharField(
                        choices=[
                            ("HA", "Happening"),
                            ("ML", "Member Led"),
                            ("CA", "Caring"),
                            ("SH", "Sharing"),
                            ("LE", "Learning"),
                            ("WO", "Working"),
                            ("DE", "Democracy"),
                        ],
                        max_length=2,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "events",
            },
        ),
        migrations.CreateModel(
            name="Interests",
            fields=[
                ("interestId", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "interests",
            },
        ),
        migrations.CreateModel(
            name="UserAttendingEvent",
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
                ("userId", models.IntegerField()),
                ("eventId", models.IntegerField()),
                ("isUserAttended", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "user_attending_event",
            },
        ),
        migrations.CreateModel(
            name="UserInterests",
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
                ("userId", models.IntegerField()),
                ("interestId", models.IntegerField()),
            ],
            options={
                "db_table": "user_interests",
            },
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "user_id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("user_name", models.CharField(max_length=45)),
                ("first_name", models.CharField(max_length=45)),
                ("last_name", models.CharField(max_length=45)),
                ("email", models.CharField(max_length=45, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("current_user_type", models.CharField(max_length=45)),
                ("have_interest_membership", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="UserTypes",
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
                ("userId", models.IntegerField()),
                ("userType", models.CharField(max_length=100)),
                ("date", models.DateTimeField()),
            ],
            options={
                "db_table": "user_types",
            },
        ),
    ]
