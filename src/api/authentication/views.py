from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, SignupSerializer, SigninSerializer
from .services.user_services import GetAllUsers, CreateNewUser, LoginUser
from . import docs


@extend_schema(**docs.user_list)
@csrf_exempt
@api_view(("GET",))
@permission_classes((IsAdminUser,))
def list_users(request: Request) -> Response:
    """
    List all users.
    """
    users = GetAllUsers().execute()
    if users:
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(**docs.signup)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def signup(request: Request) -> Response:
    """
    Create a new user.
    """
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = CreateNewUser().execute(**serializer.validated_data)
        except ValueError:
            return Response("User already exists", status=status.HTTP_409_CONFLICT)

        if user:
            return Response(status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(**docs.signin)
@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def signin(request: Request) -> Response:
    """
    Login a user.
    """
    serializer = SigninSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = LoginUser().execute(**serializer.validated_data)
        if user:
            response = Response()
            response.set_cookie(
                key="refreshtoken", value=user["refresh_token"], httponly=True
            )
            response.data = {
                "access_token": user["access_token"],
                "refresh_token": user["refresh_token"],
            }
            response.status = status.HTTP_200_OK
            return response

    return Response(status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(TokenRefreshView):
    @extend_schema(**docs.token_refresh)
    @csrf_exempt
    @permission_classes((IsAuthenticated,))
    def post(self, request: Request) -> Response:
        """
        Refresh a token.
        """
        refresh = request.data.get("refresh")

        try:
            token = RefreshToken(refresh)
            data = {
                "access": str(token.access_token),
                "refresh": str(token),
            }
            return Response(data, status=status.HTTP_200_OK)

        except TokenError:
            return Response(
                {"detail": "Token has expired or is invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
