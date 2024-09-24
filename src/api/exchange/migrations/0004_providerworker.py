# Generated by Django 5.0.6 on 2024-09-22 02:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0003_rename_active_exchangeprovider_as_main"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProviderWorker",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("url", models.URLField()),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exchange.exchangeprovider",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
