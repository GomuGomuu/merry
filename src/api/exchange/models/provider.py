from api.core.models import AbstractProvider
from api.exchange.provider import ProviderServiceInterface
from django.db import models


class ExchangeProvider(AbstractProvider):
    as_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.as_main:
            ExchangeProvider.objects.filter(as_main=True).update(as_main=False)
        super().save(*args, **kwargs)

    @property
    def service(self):
        return (self.module.service.ProviderService or ProviderServiceInterface)(self)

    def get_illustration_price(self, illustration, source_url=None):
        worker_url = self.worker.first().url
        return self.service.get_price(
            source_url=source_url,
            illustration_name=illustration.name(),
            worker_url=worker_url,
        )
