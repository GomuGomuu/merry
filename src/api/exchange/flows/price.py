from api.card.models import CardIllustration
from api.core.utils import get_days_range


def get_price_history(illustration_id, date_from=None, date_to=None, provider_id=None):
    if not date_from or not date_to:
        date_from, date_to = get_days_range()

    query = {"exchange__as_main": True}

    if provider_id:
        query["exchange__id"] = provider_id
        query.pop("exchange__as_main") if "exchange__as_main" in query else None

    services = (
        CardIllustration.objects.get(id=illustration_id)
        .connections.filter(**query)
        .first()
    )

    if services:
        return services.exchange.service.get_price_history(
            illustration_id=illustration_id, date_from=date_from, date_to=date_to
        )
    return None
