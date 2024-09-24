from django.db import models

from api.core.models import BaseModel


class ProviderWorker(BaseModel):
    provider = models.ForeignKey("exchange.ExchangeProvider", on_delete=models.CASCADE)
    url = models.URLField()
