from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        name = attrs.get("name")
        if username and password and name:
            return {
                "username": username,
                "password": password,
                "name": name,
            }
        else:
            raise serializers.ValidationError(
                "Must include 'username' and 'password' and 'name'."
            )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        if username and password:
            return {
                "username": username,
                "password": password,
            }
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "password",
            "username",
        )
