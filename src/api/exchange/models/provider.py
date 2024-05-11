from api.core.models import AbstractProvider
from api.exchange.provider import ProviderServiceInterface


class ExchangeProvider(AbstractProvider):

    @property
    def service(self):
        return (self.module.service.ProviderService or ProviderServiceInterface)(self)
