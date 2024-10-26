from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from config.settings import BASE_DIR
from .docs import card_recognition as card_recognition_docs
from .serializers.card import ImageCardSerializer
from .services.cards import CardMatcher
from .services.gemini import GeminiService
from ..card.models import Card
from ..card.serializers.card import CardSerializerList
from ..core.utils import save_image_to_disk, delete_image_from_disk

gemini = GeminiService()
card_matcher = CardMatcher()


@csrf_exempt
@api_view(("POST",))
@extend_schema(**card_recognition_docs)
@permission_classes((AllowAny,))
def card_recognition(request):
    serializer = ImageCardSerializer(data=request.data)
    if serializer.is_valid():
        image = serializer.validated_data["image"]
        image_path = save_image_to_disk(image, f"{BASE_DIR}/media/tmp/{image.name}")

        gemini_response = gemini.get_card_text_from_image(image_path)

        if gemini_response:
            card_matcher_response = card_matcher.find_closest_cards(gemini_response)
            cards = Card.objects.filter(
                slug__in=[card["slug"] for card in card_matcher_response]
            )
            response = CardSerializerList(cards, many=True)

            delete_image_from_disk(image_path)
            return Response(response.data, status=status.HTTP_200_OK)

        else:
            return Response(
                {"error": "Error extracting text from image"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
