# Generated by Django 5.0.6 on 2024-10-26 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("card", "0007_alter_cardillustration_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="cardillustration",
            name="visual_description",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
