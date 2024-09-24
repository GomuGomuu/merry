from django.contrib import admin
from api.exchange.models import ExchangeProvider, ProviderWorker
from api.exchange.models.card_conection import CardConnection


@admin.register(ExchangeProvider)
class ExchangeProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "as_main")
    fields = ("name", "app_label", "as_main")


@admin.register(CardConnection)
class CardConnectionAdmin(admin.ModelAdmin):
    fields = ("card_illustration", "exchange", "external_source_link")
    list_display = ("card_illustration", "exchange")
    list_filter = ("exchange",)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["card_illustration", "exchange"]
        else:
            return []


@admin.register(ProviderWorker)
class ProviderWorkerAdmin(admin.ModelAdmin):
    list_display = ("provider", "url")
    fields = ("provider", "url")
    list_filter = ("provider",)
