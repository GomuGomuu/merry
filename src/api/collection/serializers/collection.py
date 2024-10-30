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


class CollectionSerializer(serializers.Serializer):
    class Meta:
        model = Collection
        fields = "__all__"
        depth = 1
