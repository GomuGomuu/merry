from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from api.card import docs
from api.card.models import Card
from api.card.serializers.card import (
    CardSerializer,
    CardSerializerList,
    CardIllustrationSerializer,
)


@extend_schema(**docs.card_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def card_list(request: Request) -> Response:
    card_list_response = CardSerializerList(Card.objects.all(), many=True)
    return Response(card_list_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.card_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def card_detail(request: Request, slug: str) -> Response:
    if card := Card.objects.get(slug=slug):
        card_response = CardSerializer(card)
        print(card_response.data)
        return Response(card_response.data, status=status.HTTP_200_OK)
    return Response("Card not found", status=status.HTTP_404_NOT_FOUND)


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
def update_card(request: Request, slug: str) -> Response:
    if card := Card.objects.get(slug=slug):
        card_serializer = CardSerializer(card, data=request.data)
        if card_serializer.is_valid():
            card_serializer.save()
            return Response(card_serializer.data, status=status.HTTP_200_OK)
        return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response("Card not found", status=status.HTTP_404_NOT_FOUND)


@extend_schema(**docs.delete_card)
@csrf_exempt
@api_view(("DELETE",))
@permission_classes((IsAdminUser,))
def delete_card(request: Request, slug: str) -> Response:
    if card := Card.objects.get(slug=slug):
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response("Card not found", status=status.HTTP_404_NOT_FOUND)


@extend_schema(**docs.illustration_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def card_illustrations(request: Request, slug: str) -> Response:
    if card := Card.objects.get(slug=slug):
        serializer = CardIllustrationSerializer(card.illustrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("Card not found", status=status.HTTP_404_NOT_FOUND)


@extend_schema(**docs.create_card_illustration)
@csrf_exempt
@api_view(("POST",))
@permission_classes((IsAuthenticated,))
def create_card_illustration(request: Request) -> Response:
    serializer = CardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(**docs.card_illustration_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def card_illustration_detail(
    request: Request, slug: str, illustration_id: int
) -> Response:
    if card := Card.objects.get(slug=slug):
        if illustration := card.illustrations.filter(id=illustration_id).exists():
            serializer = CardIllustrationSerializer(illustration, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Illustration not found", status=status.HTTP_404_NOT_FOUND)
    return Response("Card not found", status=status.HTTP_404_NOT_FOUND)


@extend_schema(**docs.illustration_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def illustration_list(request: Request) -> Response:
    serializer = CardIllustrationSerializer(Card.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
