from rest_framework import serializers

from api.card.models import Card, Op, DeckColor, ArtType, Type, Crew


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class OpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Op
        fields = "__all__"


class DeckColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckColor
        fields = "__all__"


class ArtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtType
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"
