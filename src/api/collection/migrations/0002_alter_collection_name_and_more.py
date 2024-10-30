# Generated by Django 5.0.6 on 2024-10-29 20:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collection", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="name",
            field=models.CharField(default="Vault", max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name="collection",
            unique_together={("user", "name")},
        ),
    ]