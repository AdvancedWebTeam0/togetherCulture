# Generated by Django 5.1.6 on 2025-03-16 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginRegistrationApp', '0008_users_address_users_date_of_birth_users_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
