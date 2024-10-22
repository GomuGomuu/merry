import json
import logging

from api.card.models import Card, CardIllustration, SideEffect

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
