# Generated by Django 5.1.6 on 2025-03-09 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loginRegistrationApp", "0004_alter_events_labels_alter_events_tags"),
        ("memberApp", "0005_benefit_membership_alter_membership_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="MembershipType",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("duration_days", models.PositiveIntegerField()),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="membership",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="membership",
            name="start_date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="membership",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="loginRegistrationApp.users",
            ),
        ),
        migrations.AddField(
            model_name="membership",
            name="membership_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="memberApp.membershiptype",
            ),
            preserve_default=False,
        ),
    ]
