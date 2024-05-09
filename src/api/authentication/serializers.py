from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# noinspection PyAbstractClass
class SignupSerializer(serializers.Serializer):
    Username = serializers.CharField()
    Password = serializers.CharField()
    Name = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("Username")
        password = attrs.get("Password")
        name = attrs.get("Name")
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


# noinspection PyAbstractClass
class SigninSerializer(serializers.Serializer):
    Username = serializers.CharField()
    Password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("Username")
        password = attrs.get("Password")
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
