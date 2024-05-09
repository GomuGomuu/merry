from drf_spectacular.utils import OpenApiExample
from rest_framework import status

from .serializers import UserSerializer, SignupSerializer, SigninSerializer

auth_tag = "Authentication"

USER_LIST_RESPONSE = OpenApiExample(
    name="User list",
    value=[
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "string",
            "password": "string",
            "username": "string",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "string",
            "password": "string",
            "username": "string",
        },
    ],
    response_only=True,
    status_codes=["200"],
)

signup = {
    "request": SignupSerializer,
    "responses": {status.HTTP_200_OK: UserSerializer},
    "summary": "Sign up",
    "tags": [auth_tag],
}

signin = {
    "request": SigninSerializer,
    "responses": {status.HTTP_200_OK: UserSerializer},
    "summary": "Sign in",
    "tags": [auth_tag],
}

user_list = {
    "request": UserSerializer,
    "responses": {status.HTTP_200_OK: UserSerializer(many=True)},
    "summary": "List all users",
    "tags": [auth_tag],
    "examples": [USER_LIST_RESPONSE],
}
