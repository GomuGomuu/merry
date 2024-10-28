from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from config.settings import BASE_DIR
from api.recognition.docs import card_recognition as card_recognition_docs
from api.recognition.serializers.card import ImageCardSerializer
from api.recognition.services.cards import CardMatcher
from api.recognition.services.gemini import GeminiService
from api.card.models import Card, CardIllustration
from api.card.serializers.card import CardSerializer, CardIllustrationSerializer
from api.core.utils import save_image_to_disk, delete_image_from_disk


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

        """
        {
            "attack": 2000,
            "counter": 1000,
            "crew": "Straw Hat Crew",
            "description": "Look at 5 cards from the top of your deck; reveal up to 1 "
                           "[Straw Hat Crew] type card other than [Nami] and add it to "
                           "your hand. Then, place the rest at the bottom of your deck "
                           "in any order.",
            "layout_description": {
                "background_color": "red",
                "border_color": "white",
                "dominant_color": "red",
                "illustration_description": "A woman with long orange hair is wearing "
                                            "a blue and green bikini top and blue pants."
                                            " She is standing on a light blue stick and "
                                            "her right hand is on her chest. She is smiling "
                                            "with a playful expression on her face. The "
                                            "background is a forest with green trees and a"
                                            " blue sky. The card is holographic.",
                "number_of_persons": 1,
            },
            "life": 1,
            "name": "Nami",
            "type": "Character",
        }
        """
        gemini_response = gemini.get_card_text_from_image(image_path)
        print(gemini_response)

        if gemini_response:
            card_matcher_response = card_matcher.find_closest_cards(gemini_response)
            delete_image_from_disk(image_path)
            cards = Card.objects.filter(
                slug__in=[card["slug"] for card in card_matcher_response]
            )

            for card in card_matcher_response:
                card["data"] = CardSerializer(cards.get(slug=card["slug"])).data
                for illustration in card["illustrations"]:
                    illustration["data"] = CardIllustrationSerializer(
                        CardIllustration.objects.get(code=illustration["code"])
                    ).data

            return Response(card_matcher_response, status=status.HTTP_200_OK)

        else:
            delete_image_from_disk(image_path)
            return Response(
                {"error": "Error extracting text from image"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)