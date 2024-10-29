import logging

from django.core.management.base import BaseCommand

from api.exchange.tasks.prices import update_card_prices

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate tensorflow dataset"

    def handle(self, *args, **options):
        update_card_prices()
