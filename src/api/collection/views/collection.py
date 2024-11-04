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
from api.collection.services.collection import add_illustration_to_collection, \
    remove_illustration_from_collection


@csrf_exempt
@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated,))
def manage_illustration_on_vault(request):
    serializer = AddToCollectionSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        illustration_slug = serializer.validated_data["illustration_slug"]
        collection_id = serializer.validated_data.get("collection_id")

        data = {
            "user": request.user,
            "illustration_slug": illustration_slug,
        }
        if collection_id:
            data["collection_id"] = collection_id

        if request.method == "POST":
            add_illustration_to_collection(**data)
            message = f"Illustration {illustration_slug} added to collection"
        elif request.method == "DELETE":
            remove_illustration_from_collection(**data)
            message = f"Illustration {illustration_slug} removed from collection"

        return Response({"message": message}, status=status.HTTP_200_OK)

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

    illustration_list = {}

    for i in illustrations:
        if illustration_list.get(i.code):
            illustration_list[i.code]["quantity"] += 1
            illustration_list[i.code]["total_price_amount"] += i.price
            illustration_list[i.code]["total_price_amount"] = round(
                illustration_list[i.code]["total_price_amount"], 2
            )
            continue

        illustration_list[i.code] = {
            "id": i.id,
            "code": i.code,
            "title": i.card.name,
            "src": str(i.src.url),
            "price": i.price,
            "type": i.art_type,
            "total_price_amount": i.price,
            "quantity": 1,
        }

    # sort illustration_list by title
    illustration_list = dict(sorted(illustration_list.items(), key=lambda item: item[1]["title"]))

    response = {
        "collection_id": collection.id,
        "collection_name": collection.name,
        "balance": collection.balance,
        "cards_quantity": collection.cards_quantity,
        "illustrations": illustration_list,
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
