# Generated by Django 5.0.6 on 2024-05-11 04:40

import django.db.models.deletion
import sorl.thumbnail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Card",
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
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("is_dom", models.BooleanField(default=False)),
                ("cost", models.PositiveIntegerField()),
                ("power", models.PositiveIntegerField()),
                ("counter_value", models.PositiveIntegerField()),
                ("effect", models.TextField(blank=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Leader", "Leader"),
                            ("Character", "Character"),
                            ("Stage", "Stage"),
                            ("Event", "Event"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "rare",
                    models.CharField(
                        choices=[
                            ("C", "Common"),
                            ("UC", "Uncommon"),
                            ("R", "Rare"),
                            ("SR", "Super Rare"),
                            ("SCR", "Secret Rare"),
                            ("L", "Leader"),
                        ],
                        max_length=3,
                    ),
                ),
                ("trigger", models.CharField(blank=True, max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Crew",
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
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="DeckColor",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Op",
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
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="SideEffect",
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
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="CardIllustration",
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
                (
                    "src",
                    sorl.thumbnail.fields.ImageField(max_length=255, upload_to="img/"),
                ),
                ("alt", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "art_type",
                    models.CharField(
                        choices=[
                            ("COMIC", "Comic"),
                            ("ANIMATION", "Animation"),
                            ("ORIGINAL_ILLUSTRATION", "Original Illustration"),
                        ],
                        max_length=100,
                    ),
                ),
                ("is_alternative_art", models.BooleanField(default=False)),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="illustrations",
                        to="card.card",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="card",
            name="crew",
            field=models.ManyToManyField(related_name="crews", to="card.crew"),
        ),
        migrations.AddField(
            model_name="card",
            name="deck_color",
            field=models.ManyToManyField(
                related_name="deck_colors", to="card.deckcolor"
            ),
        ),
        migrations.AddField(
            model_name="card",
            name="op",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="card.op"
            ),
        ),
        migrations.AddField(
            model_name="card",
            name="side_effects",
            field=models.ManyToManyField(
                related_name="side_effects", to="card.sideeffect"
            ),
        ),
    ]
