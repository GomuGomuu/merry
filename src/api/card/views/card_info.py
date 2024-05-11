from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from api.card import docs
from api.card.models import Card, Op, DeckColor, ArtType, Type, Crew
from api.card.serializers.card import (
    OpSerializer,
    DeckColorSerializer,
    ArtTypeSerializer,
    TypeSerializer,
    CrewSerializer,
)


@extend_schema(**docs.op_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def op_list(request: Request) -> Response:
    card_list_response = OpSerializer(Card.objects.all(), many=True)
    return Response(card_list_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.op_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def op_detail(request: Request, pk: int) -> Response:
    card_detail_response = OpSerializer(Op.objects.get(pk=pk))
    return Response(card_detail_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.deck_color_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def deck_color_list(request: Request) -> Response:
    deck_color_list_response = DeckColorSerializer(DeckColor.objects.all(), many=True)
    return Response(deck_color_list_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.deck_color_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def deck_color_detail(request: Request, pk: int) -> Response:
    deck_color_detail_response = DeckColorSerializer(DeckColor.objects.get(pk=pk))
    return Response(deck_color_detail_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.art_type_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def art_type_list(request: Request) -> Response:
    art_type_list_response = ArtTypeSerializer(ArtType.objects.all(), many=True)
    return Response(art_type_list_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.art_type_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def art_type_detail(request: Request, pk: int) -> Response:
    art_type_detail_response = ArtTypeSerializer(ArtType.objects.get(pk=pk))
    return Response(art_type_detail_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.type_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def type_list(request: Request) -> Response:
    type_list_response = TypeSerializer(Type.objects.all(), many=True)
    return Response(type_list_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.type_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def type_detail(request: Request, pk: int) -> Response:
    type_detail_response = TypeSerializer(Type.objects.get(pk=pk))
    return Response(type_detail_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.crew_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def crew_list(request: Request) -> Response:
    crew_list_response = CrewSerializer(Crew.objects.all(), many=True)
    return Response(crew_list_response.data, status=status.HTTP_200_OK)


@extend_schema(**docs.crew_detail)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def crew_detail(request: Request, pk: int) -> Response:
    crew_detail_response = CrewSerializer(Crew.objects.get(pk=pk))
    return Response(crew_detail_response.data, status=status.HTTP_200_OK)
