from rest_framework import serializers


class IllustrationProviderSerializer(serializers.Serializer):
    name = serializers.CharField(source="exchange__name")
    id = serializers.IntegerField(source="exchange__id")
    main = serializers.BooleanField(source="exchange__as_main")

    class Meta:
        fields = ["name", "id", "main"]
