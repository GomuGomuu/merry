from rest_framework import serializers

from api.card.models import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["price", "date"]
