from api.card.models import CardIllustration


def update_card_price(illustration: CardIllustration):
    try:
        connection = (
            illustration.connections.filter(exchange__as_main=True).first()
        )
        price_data = connection.get_price()
        illustration.prices.create(price=price_data.get("price"))
    except Exception as e:
        raise e
