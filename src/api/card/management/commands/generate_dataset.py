import logging

from django.core.management.base import BaseCommand

from api.card.services.exporter import generate_tensorflow_dataset

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate tensorflow dataset"

    def handle(self, *args, **options):
        generate_tensorflow_dataset()
