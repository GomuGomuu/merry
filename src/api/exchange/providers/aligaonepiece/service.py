from api.exchange.providers.aligaonepiece import api
from api.exchange.providers.aligaonepiece.models.price import ProviderPrice
from api.exchange.provider import ProviderServiceInterface


class ProviderService(ProviderServiceInterface):
    def get_price_history(self, illustration_id, date_from, date_to):
        return ProviderPrice.objects.filter(
            card_illustration_id=illustration_id,
            date__range=[date_from, date_to],
        ).order_by("date")

    def get_price(self, source_url: str, illustration_name: str, worker_url: str):

        body = {
            "url": source_url,
            "card_name": illustration_name,
        }

        return api.endpoints.get_price(
            url=worker_url,
            body=body,
        )
