# serializers.py
from rest_framework import serializers


class ImageCardSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        # Aqui, você pode adicionar validações personalizadas, como o tamanho da imagem
        if value.size > 5 * 1024 * 1024:  # Limite de 5 MB
            raise serializers.ValidationError(
                "A imagem é muito grande. O limite é de 5 MB."
            )
        return value
