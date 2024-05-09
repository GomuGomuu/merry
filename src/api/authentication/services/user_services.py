from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from api.authentication.models import User
from api.authentication.utils.token import generate_access_token, generate_refresh_token
from api.core.services.base import BaseService


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
            raise AuthenticationFailed

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        return {"access_token": access_token, "refresh_token": refresh_token}
