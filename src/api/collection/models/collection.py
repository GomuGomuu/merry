from api.authentication.models import User
from api.card.models import CardIllustration
from api.core.models import BaseModel
from django.db import models


class CollectionIllustration(BaseModel):
    collection = models.ForeignKey(
        "Collection", on_delete=models.CASCADE, related_name="collection_illustrations"
    )
    illustration = models.ForeignKey(CardIllustration, on_delete=models.CASCADE)


class Collection(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=100, default="Vault")
    illustrations = models.ManyToManyField(
        CardIllustration,
        through="CollectionIllustration",
        related_name="collections",
    )

    class Meta:
        unique_together = ["user", "name"]

    def __str__(self):
        return f"{self.user.name} - {self.name}"

    @property
    def balance(self):
        _balance = 0
        for collection_illustration in self.collection_illustrations.all():
            if collection_illustration.illustration.prices.exists():
                _balance += collection_illustration.illustration.prices.last().price

        return _balance

    @property
    def cards_quantity(self):
        return self.illustrations.count()
