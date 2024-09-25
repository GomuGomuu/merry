from api.core.constants import HTTP_METHODS
from api.exchange.providers.aligaonepiece.api.constants import API_ENDPOINTS
from api.exchange.providers.aligaonepiece.api.request import request


def get_price(url: str, body: dict):
    endpoint = API_ENDPOINTS.GET_PRICE

    return request(
        url=url,
        method=HTTP_METHODS.POST,
        endpoint=endpoint,
        body=body,
    )
