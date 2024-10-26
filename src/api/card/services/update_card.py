import json
import logging

from django.db import transaction

from api.card.models import Card, CardIllustration, SideEffect
from api.card.schemas.illustration import IllustrationVisualDescription
from api.recognition.services.gemini import GeminiService
from config import settings

logger = logging.getLogger(__name__)


def update_illustration_type():
    with open(
        "initialdata/card_data.json", "r", encoding="utf-8", errors="replace"
    ) as file:
        try:
            data = json.load(file)

            for card_data in data:
                try:
                    card = Card.objects.get(slug=card_data["id"])

                    code = card_data.get("id")
                    if illustration_alternative_id := card_data.get(
                        "illustration_alternative_id"
                    ):
                        code = f"{code}_{illustration_alternative_id}"

                    illustration = CardIllustration.objects.get(
                        card=card,
                        code=code,
                        external_link=card_data["illustration_url"],
                    )

                    art_type = next(
                        (
                            choice[0]
                            for choice in CardIllustration.types
                            if choice[1] == card_data.get("illustration_type")
                        ),
                        "ORIGINAL_ILLUSTRATION",
                    )

                    illustration.art_type = art_type
                    illustration.is_alternative_art = (
                        True if art_type == "ORIGINAL_ILLUSTRATION" else False
                    )
                    illustration.save()

                    print(
                        f"Illustration {illustration} updated with type {art_type} "
                        f"and alternative art {illustration.is_alternative_art}"
                    )

                except Exception as e:
                    print(f"Error processing card {card_data.get('id')}: {e}")

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return


def update_card_effects():
    all_cards = Card.objects.all()

    side_effects = [effect.name for effect in SideEffect.objects.all()]
    for card in all_cards:
        for effect in side_effects:
            if effect.lower() in card.effect.lower():
                card.side_effects.add(SideEffect.objects.get(name=effect))
                print(f"Card {card} updated with effect {effect}")

        card.save()


def update_illustration_visual_description():
    all_illustrations = CardIllustration.objects.filter(visual_description__isnull=True)
    if not all_illustrations:
        logger.info("All illustrations already have visual description")
        return

    gemini1 = GeminiService(api_key=settings.GEMINI_API_KEY)
    gemini2 = GeminiService(api_key="another_api_key")

    error_gemini1_count = 0
    error_gemini2_count = 0

    for index, illustration in enumerate(all_illustrations):
        gemini = gemini1 if index % 2 == 0 else gemini2
        gemini_name = "Gemini1:: " if gemini == gemini1 else "Gemini2:: "
        with transaction.atomic():
            try:
                logger.info(
                    f"{gemini_name}Updating visual description for illustration {illustration}"
                )
                visual_description = gemini.get_description_from_image(
                    illustration.src.path
                )
                logger.info(
                    f"{gemini_name}Visual description extracted {str(visual_description)[:100]}..."
                )
                description = IllustrationVisualDescription(visual_description)
                illustration.set_visual_description(description)

                logger.info(
                    f"{gemini_name}Visual description updated for illustration {illustration}"
                )

                if gemini == gemini1:
                    error_gemini1_count = 0
                else:
                    error_gemini2_count = 0
            except Exception as e:
                logger.error(
                    f"Error updating visual description for illustration {illustration}: {e}"
                )
                if gemini == gemini1:
                    error_gemini1_count += 1
                else:
                    error_gemini2_count += 1

                if error_gemini1_count > 10 and error_gemini2_count > 10:
                    print("Too many errors, aborting...")
                    break
