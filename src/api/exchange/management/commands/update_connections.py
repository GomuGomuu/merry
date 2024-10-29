import csv
import logging

from django.core.management.base import BaseCommand

from api.card.models import CardIllustration
from api.exchange.models import CardConnection

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate tensorflow dataset"

    def handle(self, *args, **options):
        with open("olop_links.csv", "r") as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader if row["alop_link"]]
            for row in rows:
                try:
                    CardConnection.objects.get_or_create(
                        card_illustration=CardIllustration.objects.get(
                            code=row["code"]
                        ),
                        exchange_id=1,
                        external_source_link=row["alop_link"],
                    )
                except CardIllustration.DoesNotExist:
                    logger.error(f"CardIllustration not found: {row['card_code']}")
                    continue
                except Exception as e:
                    logger.error(f"Error: {e}")
                    continue
