from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

from api.card.models import CardIllustration
from api.core.utils import get_days_range
from api.exchange.flows.price import get_price_history
from api.exchange.serializers.ilustration_providers import (
    IllustrationProviderSerializer,
)
from api.exchange.serializers.price import PriceSerializer


@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def available_exchanges(request: Request, illustration_id: int) -> Response:
    response = {
        "illustration_id": illustration_id,
    }

    provider_list_response = CardIllustration.objects.get(
        id=illustration_id
    ).connections.values(
        "exchange__name",
        "exchange__id",
        "exchange__as_main",
    )

    response["data"] = IllustrationProviderSerializer(
        provider_list_response, many=True
    ).data

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def price_history(
    request: Request, illustration_id: int, provider_id: int = None
) -> Response:
    request_query = request.query_params
    date_from, date_to = get_days_range(
        request_query.get("date_from"), request_query.get("date_to")
    )

    response = {
        "illustration_id": illustration_id,
        "date_from": date_from,
        "date_to": date_to,
        "provider_id": provider_id if provider_id else "default",
    }
    if provider_id:
        response["provider_id"] = provider_id

    history = get_price_history(
        illustration_id=illustration_id,
        date_from=date_from,
        date_to=date_to,
        provider_id=provider_id,
    )
    if history:
        serializer = PriceSerializer(history, many=True)
        response["data"] = serializer.data

        return Response(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
