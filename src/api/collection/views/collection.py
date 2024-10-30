from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.collection.serializers.collection import (
    AddToCollectionSerializer,
    GetCollectionSerializer,
)

from rest_framework import status
from rest_framework.response import Response

from api.collection.services.collection import get_collection_illustration


@csrf_exempt
@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def add_illustration_to_collection(_request):
    serializer = AddToCollectionSerializer(data=_request.data)

    if serializer.is_valid(raise_exception=True):
        add_illustration_to_collection(
            user=_request.user,
            illustration_slug=serializer.validated_data["illustration_slug"],
            collection_id=serializer.validated_data["collection_id"],
        )

        return Response(
            {
                "message": f"Illustration {serializer.validated_data['illustration_slug']} "
                f"added to collection"
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def get_collection_illustrations(_request):
    collection_id = _request.query_params.get("collection_id")
    if collection_id:
        GetCollectionSerializer(data=_request.data).is_valid(raise_exception=True)

    collection = get_collection_illustration(
        user=_request.user, collection_id=collection_id
    )
