from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

from .serializers import ProjectSerializer


@csrf_exempt
@api_view(("POST",))
@permission_classes((AllowAny,))
def project_test(request: Request) -> Response:
    """
    View function for project_test page
    """
    serializer = ProjectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(status=status.HTTP_200_OK)
