from api.card.models import CardIllustration
import logging

logger = logging.getLogger(__name__)


def update_card_price(illustration: CardIllustration):
    try:
        logger.info(f"Updating price for {illustration.code}")
        connection = illustration.connections.filter(exchange__as_main=True).first()
        price_data = connection.get_price()
        logger.info(
            f"Illustration: {illustration.code} - Price: {price_data.get('price')}"
        )
        illustration.prices.create(price=price_data.get("price"))
    except Exception as e:
        logger.error(f"[Error] Card: {illustration.code} - {e}")
        raise e
