from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from api.card import docs
from api.card.models import Card
from api.card.serializers.card import CardSerializer


@extend_schema(**docs.card_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def card_list(request: Request) -> Response:
    card_list_response = CardSerializer(Card.objects.all(), many=True)
    return Response(card_list_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.card_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def card_detail(request: Request, card_id: int) -> Response:
    card = Card.objects.get(id=card_id)
    card_response = CardSerializer(card)
    return Response(card_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.create_card)
@csrf_exempt
@api_view(("POST",))
@permission_classes((IsAuthenticated,))
def create_card(request: Request) -> Response:
    card = CardSerializer(data=request.data)
    if card.is_valid():
        card.save()
        return Response(card.data, status=status.HTTP_201_CREATED)
    return Response(card.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(**docs.update_card)
@csrf_exempt
@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def update_card(request: Request, card_id: int) -> Response:
    card = Card.objects.get(id=card_id)
    card_serializer = CardSerializer(card, data=request.data)
    if card_serializer.is_valid():
        card_serializer.save()
        return Response(card_serializer.data, status=status.HTTP_200_OK)
    return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(**docs.delete_card)
@csrf_exempt
@api_view(("DELETE",))
@permission_classes((IsAdminUser,))
def delete_card(request: Request, card_id: int) -> Response:
    card = Card.objects.get(id=card_id)
    card.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
