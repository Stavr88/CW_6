# Generated by Django 4.2.2 on 2024-09-14 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("email_list", "0002_client_owner_mailingmessage_owner_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailingsettings",
            options={
                "permissions": [("stop_mailing", "Can stop mailing")],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
    ]
