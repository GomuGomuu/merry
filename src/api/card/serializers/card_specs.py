from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

from api.card.models import Op, DeckColor, ArtType, Type, Crew
from api.card.serializers.card import (
    OpSerializer,
    DeckColorSerializer,
    ArtTypeSerializer,
    TypeSerializer,
    CrewSerializer,
)


# @extend_schema(**docs.op_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def op_list(request: Request) -> Response:
    op_list_response = OpSerializer(Op.objects.all(), many=True)
    return Response(op_list_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.get_op)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def get_op(request: Request, op_id: int) -> Response:
    op = Op.objects.get(id=op_id)
    op_response = OpSerializer(op)
    return Response(op_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.deck_color_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def deck_color_list(request: Request) -> Response:
    deck_color_list_response = DeckColorSerializer(DeckColor.objects.all(), many=True)
    return Response(deck_color_list_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.get_deck_color)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def get_deck_color(request: Request, deck_color_id: int) -> Response:
    deck_color = DeckColor.objects.get(id=deck_color_id)
    deck_color_response = DeckColorSerializer(deck_color)
    return Response(deck_color_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.art_type_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def art_type_list(request: Request) -> Response:
    art_type_list_response = ArtTypeSerializer(ArtType.objects.all(), many=True)
    return Response(art_type_list_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.get_art_type)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def get_art_type(request: Request, art_type_id: int) -> Response:
    art_type = ArtType.objects.get(id=art_type_id)
    art_type_response = ArtTypeSerializer(art_type)
    return Response(art_type_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.type_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def type_list(request: Request) -> Response:
    type_list_response = TypeSerializer(Type.objects.all(), many=True)
    return Response(type_list_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.get_type)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def get_type(request: Request, type_id: int) -> Response:
    type = Type.objects.get(id=type_id)
    type_response = TypeSerializer(type)
    return Response(type_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.crew_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def crew_list(request: Request) -> Response:
    crew_list_response = CrewSerializer(Crew.objects.all(), many=True)
    return Response(crew_list_response.data, status=status.HTTP_200_OK)


# @extend_schema(**docs.get_crew)
@csrf_exempt
@api_view(("GET",))
@permission_classes((AllowAny,))
def get_crew(request: Request, crew_id: int) -> Response:
    crew = Crew.objects.get(id=crew_id)
    crew_response = CrewSerializer(crew)
    return Response(crew_response.data, status=status.HTTP_200_OK)
