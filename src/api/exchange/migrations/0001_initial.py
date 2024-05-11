# Generated by Django 5.0.6 on 2024-05-11 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("card", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeProvider",
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
                ("name", models.CharField(max_length=30, unique=True)),
                ("app_label", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CardConnection",
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
                ("external_source_link", models.URLField(blank=True, null=True)),
                (
                    "card_illustration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="card.cardillustration",
                    ),
                ),
                (
                    "exchange",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exchange.exchangeprovider",
                    ),
                ),
            ],
            options={
                "verbose_name": "Card Connection",
                "verbose_name_plural": "Card Connections",
                "db_table": "card_connection",
                "unique_together": {("card_illustration", "exchange")},
            },
        ),
    ]