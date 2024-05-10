import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

logger = logging.getLogger(__name__)


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


def create_image_tags():
    from api.card.models import Tag

    if not Tag.objects.exists():
        Tag.objects.create(name="Principal Art", slug="principal-art")
        Tag.objects.create(name="Alternative Art", slug="alternative-art")


def create_card_types():
    from api.card.models import Type

    if not Type.objects.exists():
        Type.objects.create(name="Leader")
        Type.objects.create(name="Character")
        Type.objects.create(name="Event")


class Command(BaseCommand):
    help = "Initialize base structure"

    def handle(self, *args, **options):
        logger.warning("Initializing base structure")

        logger.warning("Creating image tags")
        create_image_tags()

        logger.warning("Creating card ops")
        create_card_ops()

        logger.warning("Creating deck colors")
        create_deck_colors()

        logger.warning("Creating card types")
        create_card_types()

        if settings.DEBUG:
            call_command("init_develop")
