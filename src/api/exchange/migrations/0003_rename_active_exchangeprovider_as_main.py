# Generated by Django 5.0.6 on 2024-05-12 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0002_exchangeprovider_active_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="exchangeprovider",
            old_name="active",
            new_name="as_main",
        ),
    ]
