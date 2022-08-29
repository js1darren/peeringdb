# Generated by Django 3.2.14 on 2022-08-18 11:33

from django.db import migrations

def forward(apps, schema_editor):

    User = apps.get_model("peeringdb_server", "User")
    EmailAddress = apps.get_model("account", "EmailAddress")

    emails = {}

    for email in EmailAddress.objects.all():
        emails.setdefault(email.user_id, [])
        emails[email.user_id].append(email.email)

    for user in User.objects.exclude(email__isnull=True).exclude(email=""):
        if user.email not in emails.get(user.id,[]):
            try:
                EmailAddress.objects.create(email=user.email, user=user, primary=True)
            except Exception as exc:
                print(f"Could not create missing email address object for user {user.username} - will need to handle manually")


class Migration(migrations.Migration):

    dependencies = [
        ('peeringdb_server', '0091_alter_user_email'),
    ]

    operations = [
        migrations.RunPython(forward, migrations.RunPython.noop)
    ]
