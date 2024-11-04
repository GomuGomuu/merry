import time

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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

gemini = GeminiService()
card_matcher = CardMatcher()


@csrf_exempt
@api_view(("POST",))
@extend_schema(**card_recognition_docs)
@permission_classes((IsAuthenticated,))
def card_recognition(request):

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
        start_gemini = time.time()
        gemini_response = gemini.get_card_text_from_image(image_path)
        print(f"Time to get text from image: {time.time() - start_gemini}")
        # gemini_response = {
        #     "attack": 5000,
        #     "counter": 2000,
        #     "description": "On Play: If you have 3 or less DON!! cards on your field, add up to 2 DON!! cards from your DON!! deck and rest them.",
        #     "layout_description": {
        #         "background_color": "red",
        #         "border_color": "white",
        #         "dominant_color": "red",
        #         "illustration_description": "Two anime characters are depicted in the illustration. One of them is a man wearing a black and white outfit, a black hat with the word 'GUN' on it, and black gloves. He is pointing his fist at the viewer. The second character is a woman wearing a black and red outfit, a black and white hat with a white whale tail on it, and holding a whale tail sword. She is standing behind the man and is pointing a finger at the viewer. ",
        #         "number_of_persons": 2,
        #     },
        #     "name": "Shachi & Penguin",
        #     "type": "CHARACTER",
        # }
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
                    card_illustration = CardIllustration.objects.get(
                        code=illustration["code"]
                    )
                    illustration["data"] = CardIllustrationSerializer(
                        card_illustration
                    ).data
                    if price := card_illustration.prices.last():
                        illustration["data"]["price"] = price.price
            return Response(card_matcher_response, status=status.HTTP_200_OK)

        else:
            delete_image_from_disk(image_path)
            return Response(
                {"error": "Error extracting text from image"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
