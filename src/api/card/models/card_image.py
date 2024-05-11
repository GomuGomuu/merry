from api.card.models.card import Card
from api.core.models.image import AbstractImage
from django.db import models


class CardIllustration(AbstractImage):
    types = [
        ("COMIC", "Comic"),
        ("ANIMATION", "Animation"),
        ("ORIGINAL_ILLUSTRATION", "Original Illustration"),
    ]

    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name="illustrations"
    )
    art_type = models.CharField(max_length=100, choices=types)
    is_alternative_art = models.BooleanField(default=False)

    def __str__(self):
        return self.card.name
