import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction

from api.card.models import Card, Op, Atribute, DeckColor, Crew, CardIllustration

logger = logging.getLogger(__name__)


def process_card(card_data):
    try:
        card = Card.objects.get(slug=card_data["id"])

        if CardIllustration.objects.filter(
            external_link=card_data["illustration_url"]
        ).exists():
            logger.info(f"Card {card.name} illustration already exists")
            return

        code = card_data.get("id")
        if illustration_alternative_id := card_data.get("illustration_alternative_id"):
            code = f"{code}_{illustration_alternative_id}"

        is_alternative_art = card_data.get("art_type") == "Original Illustrations"
        art_type = next(
            (
                choice[0]
                for choice in CardIllustration.types
                if choice[0] == card_data.get("illustration_type")
            ),
            "ORIGINAL_ILLUSTRATION",
        )

        illustration = CardIllustration.objects.create(
            card=card,
            code=code,
            art_type=art_type,
            is_alternative_art=is_alternative_art,
            external_link=card_data.get("illustration_url"),
        )
        logger.info(f"Illustration {illustration} created")

        illustration.set_image_from_url(card_data.get("illustration_url"))
        illustration.save()
        logger.info(f"Illustration {illustration} updated")

    except Exception as e:
        logger.error(f"Error processing card {card_data.get('id')}: {e}")


def _download_illustration(data, num_workers=4):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_card, card_data) for card_data in data]

        for future in as_completed(futures):
            try:
                future.result()  # Reraise exceptions
            except Exception as e:
                logger.error(f"Error in thread: {e}")


def import_card(import_images=False):
    def clean_json_content(content):
        return re.sub(r"[^\x00-\x7F]+", "", content)

    with open(
        "initialdata/card_data.json", "r", encoding="utf-8", errors="replace"
    ) as file:
        try:
            raw_content = file.read()
            cleaned_content = clean_json_content(raw_content)
            data = json.loads(cleaned_content)

            for card_data in data:
                try:
                    with transaction.atomic():
                        card = Card.objects.filter(slug=card_data["id"]).first()
                        if not card:
                            logger.info(f"Creating card {card_data['name']}")
                            cost = card_data.get("cost")
                            power = card_data.get("power")
                            counter_value = card_data.get("counter_value")

                            valid_rare_choices = [
                                choice[0] for choice in Card.RARE_CHOICES
                            ]
                            rare_value = card_data.get("rare", "C")
                            if rare_value not in valid_rare_choices:
                                rare_value = "C"

                            card = Card(
                                slug=card_data["id"],
                                name=card_data.get("name"),
                                is_dom=card_data.get("is_dom", False),
                                cost=int(cost) if cost else 0,
                                power=int(power) if power else 0,
                                effect=card_data.get("effect"),
                                counter_value=(
                                    int(counter_value) if counter_value else 0
                                ),
                                rare=rare_value,
                                trigger=card_data.get("trigger"),
                                type=card_data.get("type"),
                            )

                            if card_data["pack_data"].get("pack_name"):
                                op, _ = Op.objects.get_or_create(
                                    name=card_data["pack_data"].get("pack_name"),
                                    slug=card_data["pack_data"].get("pack_code"),
                                )
                                card.op = op
                            else:
                                card.op = Op.objects.get_or_create(
                                    name="Unknown", slug="unknown"
                                )[0]

                            if atribute := card_data.get("attribute"):
                                if atribute := Atribute.objects.filter(
                                    name=atribute
                                ).first():
                                    card.atribute = atribute
                                else:
                                    atribute = Atribute.objects.create(name=atribute)
                                    atribute.set_image_from_url(
                                        card_data.get("attribute_image_url")
                                    )
                                    card.atribute = atribute

                            card.save()

                            color = card_data.get("color").split("/")
                            for c in color:
                                color, _ = DeckColor.objects.get_or_create(
                                    name=c.title()
                                )
                                card.deck_color.add(color)

                            for crew in card_data.get("crew"):
                                crew, _ = Crew.objects.get_or_create(name=crew)
                                card.crew.add(crew)

                            logger.info(f"Card {card.name} updated")

                except Exception as e:
                    raise e

            if import_images:
                _download_illustration(data, num_workers=4)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return


def import_card_illustrations():
    with open(
        "initialdata/card_data.json", "r", encoding="utf-8", errors="replace"
    ) as file:
        try:
            data = json.load(file)

            _download_illustration(data, num_workers=4)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return


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
