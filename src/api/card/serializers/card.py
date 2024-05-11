from rest_framework import serializers

from api.card.models import Card, Op, DeckColor, Crew, CardIllustration


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        # add all fields plus to_representation method
        fields = "__all__"
        depth = 1

    def get_fields(self):
        fields = super().get_fields()
        fields["op"] = OpSerializer()
        fields["deck_color"] = DeckColorSerializer()
        fields["crew"] = CrewSerializer()
        return fields


class CardSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["illustrations"] = CardIllustrationSerializer(
            instance.illustrations, many=True
        ).data
        return representation


class CardIllustrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardIllustration
        fields = "__all__"


class OpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Op
        fields = "__all__"


class DeckColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckColor
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"
