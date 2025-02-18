from django.db import migrations

#Load the initial data for interests to database at the beginning
def load_initial_interests(apps, schema_editor):
    Interests = apps.get_model("loginPage", "Interests")
    db_alias = schema_editor.connection.alias
    
    Interests.objects.using(db_alias).bulk_create([
        Interests(interestId = 1, name = "Happening"),
        Interests(interestId = 2, name = "Member Led"),
        Interests(interestId = 3, name = "Caring"),
        Interests(interestId = 4, name = "Sharing"),
        Interests(interestId = 5, name = "Learning"),
        Interests(interestId = 6, name = "Working"),
        Interests(interestId = 7, name = "Democracy"),
    ])


class Migration(migrations.Migration):
    dependencies = [
        ("loginPage", "0003_events_interests_userattendingevent_userinterests"),
    ]

    operations = [
        migrations.RunPython(load_initial_interests),
    ]
