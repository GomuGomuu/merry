from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from api.authentication.models import User
from api.core.services.base import BaseService
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetAllUsers(BaseService):
    def execute(self):
        return User.objects.get_all_users()


class CreateNewUser(BaseService):
    def execute(self, name: str, password: str, username: str):
        return User.objects.create_user(
            name=name,
            password=password,
            username=username,
        )


class LoginUser(BaseService):
    def execute(self, username: str, password: str):
        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid username or password")

        token_serializer = TokenObtainPairSerializer(
            data={"username": username, "password": password}
        )
        token_serializer.is_valid(raise_exception=True)

        return {
            "access_token": token_serializer.validated_data["access"],
            "refresh_token": token_serializer.validated_data["refresh"],
        }
