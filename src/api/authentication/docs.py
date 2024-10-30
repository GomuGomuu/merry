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
    ],
    response_only=True,
    status_codes=["200"],
)

SIGNUP_REQUEST_EXAMPLE = OpenApiExample(
    name="Sign Up",
    value={
        "name": "John Doe",
        "username": "johndoe",
        "password": "securepassword123",
    },
    request_only=True,
    status_codes=["201"],
)

SIGNIN_REQUEST_EXAMPLE = OpenApiExample(
    name="Sign In",
    value={
        "username": "johndoe",
        "password": "securepassword123",
    },
    request_only=True,
    status_codes=["200"],
)

REFRESH_REQUEST_EXAMPLE = OpenApiExample(
    name="Token Refresh",
    value={"refresh": "your_refresh_token_here"},
    request_only=True,
    status_codes=["200"],
)

REFRESH_RESPONSE_EXAMPLE = OpenApiExample(
    name="Token Refresh Response",
    value={"access": "new_access_token_here", "refresh": "new_refresh_token_here"},
    response_only=True,
    status_codes=["200"],
)

signup = {
    "request": SignupSerializer,
    "responses": {status.HTTP_200_OK: UserSerializer},
    "summary": "Sign up",
    "tags": [auth_tag],
    "examples": [SIGNUP_REQUEST_EXAMPLE],
}

signin = {
    "request": SigninSerializer,
    "responses": {status.HTTP_200_OK: UserSerializer},
    "summary": "Sign in",
    "tags": [auth_tag],
    "examples": [SIGNIN_REQUEST_EXAMPLE],
}

user_list = {
    "request": UserSerializer,
    "responses": {status.HTTP_200_OK: UserSerializer(many=True)},
    "summary": "List all users",
    "tags": [auth_tag],
    "examples": [USER_LIST_RESPONSE],
}

token_refresh = {
    "request": {"refresh": "string"},
    "responses": {
        status.HTTP_200_OK: {
            "access": "string",
            "refresh": "string",
        },
        status.HTTP_401_UNAUTHORIZED: {"detail": "Token has expired or is invalid."},
    },
    "summary": "Refresh access and refresh tokens",
    "tags": [auth_tag],
    "examples": [REFRESH_REQUEST_EXAMPLE, REFRESH_RESPONSE_EXAMPLE],
}
