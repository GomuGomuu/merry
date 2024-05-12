from django.db import models

from api.card.models import CardIllustration


class Price(models.Model):
    card_illustration = models.ForeignKey(CardIllustration, on_delete=models.PROTECT)
    price = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return str(self.price)
