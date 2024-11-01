from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.collection.models import Collection
from api.collection.serializers.collection import (
    AddToCollectionSerializer,
    CollectionSerializer,
)

from rest_framework import status
from rest_framework.response import Response
from api.collection import docs


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
@extend_schema(**docs.collection)
@permission_classes((IsAuthenticated,))
def get_collection(_request, collection_id=None):
    if not collection_id:
        collection = Collection.objects.get(user=_request.user, name="Vault")
    else:
        collection = Collection.objects.get(user=_request.user, id=collection_id)

    illustrations = collection.illustrations.all()
    """
        op12-001: {
            "id": 1,
            "slug": "op12-001",
            "title": "Luffy",
            "image": "https://example.com/image.jpg",
            "price": 1.23,
            "quantity": 43,
        }
    """

    ilustration_list = {}

    for i in illustrations:
        if ilustration_list.get(i.code):
            ilustration_list[i.code]["quantity"] += 1
            ilustration_list[i.code]["total_price_amount"] += i.price
            ilustration_list[i.code]["total_price_amount"] = round(
                ilustration_list[i.code]["total_price_amount"], 2
            )
            continue

        ilustration_list[i.code] = {
            "id": i.id,
            "code": i.code,
            "title": i.card.name,
            "src": str(i.src.url),
            "price": i.price,
            "type": i.art_type,
            "total_price_amount": i.price,
            "quantity": 1,
        }

    response = {
        "collection_id": collection.id,
        "collection_name": collection.name,
        "balance": collection.balance,
        "cards_quantity": collection.cards_quantity,
        "illustrations": ilustration_list,
    }

    return Response(response, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def collections(_request):
    try:
        collections = Collection.objects.filter(user=_request.user)
    except Collection.DoesNotExist:
        return Response(
            {"error": "No collections found for this user"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CollectionSerializer(collections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
