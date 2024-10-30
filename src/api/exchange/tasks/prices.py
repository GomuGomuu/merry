from django.utils import timezone
import time
from api.card.services.update_price import update_card_price
from api.exchange.models import CardConnection
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


def update_card_prices():
    exchange_id = 1
    update_list = CardConnection.objects.filter(exchange_id=exchange_id)

    update_list = update_list.exclude(
        id__in=[
            connection.id
            for connection in update_list
            if connection.card_illustration.prices.filter(
                date__gt=timezone.now() - timedelta(days=1)
            ).exists()
        ]
    )

    retry_card_left = 0
    while update_list.exists():
        logger.info(
            f"Updating {update_list.count()} card prices, total retry left: {retry_card_left}"
        )

        for connection in update_list:
            try:
                update_card_price(connection.card_illustration)
                time.sleep(1)
            except Exception as e:
                retry_card_left += 1
                logger.error(f"Error updating card price: {e}")
                time.sleep(1)
            update_list = update_list.exclude(id=connection.id)
