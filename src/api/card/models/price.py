from django.db import models

from api.card.models import CardIllustration


class Price(models.Model):
    card_illustration = models.ForeignKey(
        CardIllustration, on_delete=models.PROTECT, related_name="prices"
    )
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.price)
