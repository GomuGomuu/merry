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
    code = models.CharField(max_length=100, unique=True)
    external_link = models.URLField(null=True, blank=True)

    class Meta:
        unique_together = ("card", "code")

    def __str__(self):
        text = f"{self.card} - {self.code} - {self.art_type}"
        if self.is_alternative_art:
            text += " (Alternative Art)"
        return text

    def name(self):
        return f"{self.card} - {self.code} - {self.art_type}"

    def to_json(self):
        return {
            "art_type": self.art_type,
            "is_alternative_art": self.is_alternative_art,
            "code": self.code,
            "external_link": self.external_link,
            "image": str(self.src),
        }
