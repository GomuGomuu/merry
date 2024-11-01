from rest_framework import serializers

from api.collection.models import Collection


class AddToCollectionSerializer(serializers.Serializer):
    collection_id = serializers.IntegerField()
    illustration_slug = serializers.CharField()

    class Meta:
        fields = ["collection_id", "illustration_slug"]

    def validate(self, data):
        if not data.get("collection_id"):
            raise serializers.ValidationError("Collection id is required")
        if not data.get("illustration_slug"):
            raise serializers.ValidationError("Illustration slug is required")
        return data


class GetCollectionSerializer(serializers.Serializer):
    collection_id = serializers.IntegerField()

    class Meta:
        fields = ["collection_id"]


class CollectionSerializer(serializers.ModelSerializer):
    cards_quantity = serializers.IntegerField(read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Collection
        fields = ["id", "name", "cards_quantity", "balance"]
