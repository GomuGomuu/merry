# Generated by Django 5.0.6 on 2024-09-24 17:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("card", "0003_price_card_illustration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="price",
            name="card_illustration",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="prices",
                to="card.cardillustration",
            ),
        ),
    ]
