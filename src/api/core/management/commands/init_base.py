import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from config.settings import BASE_DIR

logger = logging.getLogger(__name__)


def create_exchange_providers():
    from api.exchange.models import ExchangeProvider

    if not ExchangeProvider.objects.exists():
        ExchangeProvider.objects.get_or_create(
            name="A Liga One Piece", app_label="exchange_aligaonepiece"
        )


def create_card_ops():
    from api.card.models import Op

    if not Op.objects.exists():
        Op.objects.create(name="Op 1", slug="op-1")
        Op.objects.create(name="Op 2", slug="op-2")
        Op.objects.create(name="Op 3", slug="op-3")
        Op.objects.create(name="Op 4", slug="op-4")
        Op.objects.create(name="Op 5", slug="op-5")
        Op.objects.create(name="Op 6", slug="op-6")
        Op.objects.create(name="Op 7", slug="op-7")
        Op.objects.create(name="Op 8", slug="op-8")
        Op.objects.create(name="Op 9", slug="op-9")


def create_deck_colors():
    from api.card.models import DeckColor

    if not DeckColor.objects.exists():
        DeckColor.objects.create(name="Blue")
        DeckColor.objects.create(name="Green")
        DeckColor.objects.create(name="Yellow")
        DeckColor.objects.create(name="Purple")
        DeckColor.objects.create(name="Red")
        DeckColor.objects.create(name="Black")
        DeckColor.objects.create(name="Multicolor")


def creat_card_crews():
    from api.card.models import Crew

    if not Crew.objects.exists():
        Crew.objects.create(name="Straw Hat", slug="straw-hat")
        Crew.objects.create(name="Supernovas", slug="supernovas")
        Crew.objects.create(name="Marines", slug="marines")
        Crew.objects.create(name="Whitebeard Pirates", slug="whitebeard-pirates")


def creat_card():
    from api.card.models import Card
    from api.card.models import Crew
    from api.card.models import DeckColor
    from api.card.models import Op
    from api.card.models import SideEffect
    from api.card.models import CardIllustration

    if not Card.objects.exists():
        zoro = Card.objects.create(
            name="Roronoa Zoro",
            slug="roronoa-zoro",
            cost=3,
            power=5000,
            counter_value=0,
            type="Character",
            rare="SR",
            op=Op.objects.get(slug="op-1"),
        )
        zoro.crew.add(
            Crew.objects.get(slug="straw-hat"), Crew.objects.get(slug="supernovas")
        )
        zoro.deck_color.add(DeckColor.objects.get(name="Red"))
        zoro.side_effects.add(SideEffect.objects.get(slug="rush"))
        zoro.save()

        illustation1 = CardIllustration.objects.create(
            card_id=1,
            art_type="ORIGINAL_ILLUSTRATION",
            is_alternative_art=True,
            code="OP01-025-PAR",
        )

        illustation1.src.save(
            "2024-05-11-1a5f2043-d9fb-45d3-adaf-79e69b637094-op01-025-par.png",
            open(f"{BASE_DIR.parent}/initialdata/OP01-025_p1.png", "rb"),
        )

        illustation2 = CardIllustration.objects.create(
            card_id=1,
            art_type="ANIMATION",
            is_alternative_art=False,
            code="OP01-025",
        )

        illustation2.src.save(
            "2024-05-11-1c089c06-14d0-4df5-81fd-7a4778caa15c-op01-025.png",
            open(f"{BASE_DIR.parent}/initialdata/OP01-025.png", "rb"),
        )


class Command(BaseCommand):
    help = "Initialize base structure"

    def handle(self, *args, **options):
        logger.warning("Initializing base structure")

        logger.warning("Creating card ops")
        create_card_ops()

        logger.warning("Creating exchange providers")
        create_exchange_providers()

        logger.warning("Creating deck colors")
        create_deck_colors()

        logger.warning("Creating card crews")
        creat_card_crews()

        logger.warning("Creating card")
        creat_card()

        if settings.DEBUG:
            call_command("init_develop")
