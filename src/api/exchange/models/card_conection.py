from api.card.models import CardIllustration
from api.core.models import BaseModel
from django.db import models

from api.exchange.models import ExchangeProvider


class CardConnection(BaseModel):
    card_illustration = models.ForeignKey(CardIllustration, on_delete=models.PROTECT)
    exchange = models.ForeignKey(ExchangeProvider, on_delete=models.CASCADE)
    external_source_link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "card_connection"
        verbose_name = "Card Connection"
        verbose_name_plural = "Card Connections"
        unique_together = ("card_illustration", "exchange")

    def __str__(self):
        return f"{self.card_illustration} :: {self.exchange}"

    @property
    def name(self):
        return self.__str__()
