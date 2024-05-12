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
