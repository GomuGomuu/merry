from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from api.exchange.models import ExchangeProvider
from api.exchange.serializers.provider import ExchangeProviderSerializer


@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def provider_list(request: Request) -> Response:
    serializer = ExchangeProviderSerializer(
        ExchangeProvider.objects.all().values("name", "id", "as_main"), many=True
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
