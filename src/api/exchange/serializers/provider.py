from rest_framework import serializers

from api.exchange.models import ExchangeProvider


class ExchangeProviderSerializer(serializers.ModelSerializer):
    main = serializers.BooleanField(source="as_main")

    class Meta:
        model = ExchangeProvider
        fields = ["id", "name", "main"]
