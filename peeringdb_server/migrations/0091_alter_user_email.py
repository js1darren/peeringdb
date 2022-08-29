# Generated by Django 3.2.14 on 2022-08-17 14:29

from django.db import migrations, models

def clean_up_dupe_email_accounts(apps, schema_editor):

    User = apps.get_model("peeringdb_server", "User")
    EmailAddress = apps.get_model("account", "EmailAddress")

    emails = {}

    deactivated = 0

    for user in User.objects.all().order_by("-last_login"):

        emails.setdefault(user.email, 0)
        emails[user.email] += 1

        if emails[user.email] > 1:
            user.is_active = False
            user.email = None
            deactivated += 1
            user.save()

            EmailAddress.objects.filter(user=user).delete()


def revert_clean_up_dupe_email_accounts(apps, schema_editor):

    User = apps.get_model("peeringdb_server", "User")
    User.objects.filter(email__isnull=True).update(email="")


class Migration(migrations.Migration):

    dependencies = [
        ('peeringdb_server', '0090_auto_20220715_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email address'),
        ),
        migrations.RunPython(clean_up_dupe_email_accounts, revert_clean_up_dupe_email_accounts),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
