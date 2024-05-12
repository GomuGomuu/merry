from django.contrib import admin

from api.exchange.providers.aligaonepiece.models import ProviderPrice


class ALigaOnePiecePriceAdmin(admin.ModelAdmin):
    list_display = ["card_illustration", "price", "date"]
    list_filter = ["date"]
    search_fields = [
        "price",
        "date",
        "card_illustration__card__name",
        "card_illustration__card__id",
        "card_illustration__id",
    ]


admin.site.register(ProviderPrice, ALigaOnePiecePriceAdmin)
