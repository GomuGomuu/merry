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
from ..core.utils import save_image_to_disk, delete_image_from_disk


@csrf_exempt
@api_view(("POST",))
@extend_schema(**card_recognition_docs)
@permission_classes((AllowAny,))
def card_recognition(request):
    gemini = GeminiService()
    card_matcher = CardMatcher()

    serializer = ImageCardSerializer(data=request.data)
    if serializer.is_valid():
        image = serializer.validated_data["image"]
        image_path = save_image_to_disk(image, f"{BASE_DIR}/media/tmp/{image.name}")

        gemini_response = gemini.get_card_text_from_image(image_path)
        print(gemini_response)
        # gemini_response = {
        #     "attack": 2000,
        #     "counter": 1000,
        #     "crew": "Straw Hat Crew",
        #     "description": "Look at 5 cards from the top of your deck; reveal up to 1 "
        #     "[Straw Hat Crew] type card other than [Nami] and add it to "
        #     "your hand. Then, place the rest at the bottom of your deck "
        #     "in any order.",
        #     "layout_description": {
        #         "background_color": "red",
        #         "border_color": "white",
        #         "dominant_color": "red",
        #         "illustration_description": "A woman with long orange hair is wearing "
        #         "a blue and green bikini top and blue pants."
        #         " She is standing on a light blue stick and "
        #         "her right hand is on her chest. She is smiling "
        #         "with a playful expression on her face. The "
        #         "background is a forest with green trees and a"
        #         " blue sky. The card is holographic.",
        #         "number_of_persons": 1,
        #     },
        #     "life": 1,
        #     "name": "Nami",
        #     "type": "Character",
        # }

        if gemini_response:
            card_matcher_response = card_matcher.find_closest_cards(gemini_response)
            delete_image_from_disk(image_path)

            return Response(card_matcher_response, status=status.HTTP_200_OK)

        else:
            delete_image_from_disk(image_path)
            return Response(
                {"error": "Error extracting text from image"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
