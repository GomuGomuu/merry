from django.contrib import admin
from django import forms
from api.card.models import CardIllustration
from api.exchange.models import ExchangeProvider
from api.exchange.models.card_conection import CardConnection


class ExchangeProviderAdmin(admin.ModelAdmin):
    fields = ("name", "app_label")


admin.site.register(ExchangeProvider, ExchangeProviderAdmin)


class CardConnectionForm(forms.ModelForm):
    class Meta:
        model = CardConnection
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["card_illustration"].queryset = CardIllustration.objects.all()
        self.fields["exchange"].queryset = ExchangeProvider.objects.all()


class CardConnectionAdmin(admin.ModelAdmin):
    fields = ("card_illustration", "exchange", "external_source_link")
    list_display = ("card_illustration", "exchange")
    list_filter = ("exchange",)
    form = CardConnectionForm


admin.site.register(CardConnection, CardConnectionAdmin)
