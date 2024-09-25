from django.db import models

from api.core.models import BaseModel


class ProviderWorker(BaseModel):
    provider = models.ForeignKey(
        "exchange.ExchangeProvider", on_delete=models.CASCADE, related_name="worker"
    )
    url = models.URLField()
