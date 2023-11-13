from django.db import migrations


def update_mood_user(apps, schema_editor):
    Mood = apps.get_model("base", "Mood")
    User = apps.get_model("auth", "User")

    # Assuming you want to assign all existing moods to the first user
    first_user = User.objects.first()
    if first_user:
        Mood.objects.update(user=first_user)


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0010_remove_mood_user_id_mood_user"),
    ]

    operations = [
        migrations.RunPython(update_mood_user),
    ]
