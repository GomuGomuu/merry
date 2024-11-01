from drf_spectacular.utils import OpenApiExample
from rest_framework import status

COLLECTION_RESPONSE_EXAMPLE = OpenApiExample(
    name="Collection Response",
    value=[
        {
            "id": 1,
            "slug": "op12-001",
            "title": "Luffy",
            "image": "https://example.com/image.jpg",
            "price": 1.23,
            "quantity": 43,
        },
    ],
    response_only=True,
    status_codes=["200"],
)

collection = {
    "request": {"collection_id": "string (optional)"},
    "responses": {
        status.HTTP_200_OK: {
            "id": "integer",
            "slug": "string",
            "title": "string",
            "image": "string (URL)",
            "price": "number",
            "quantity": "integer",
        },
        status.HTTP_404_NOT_FOUND: {"detail": "Collection or illustrations not found."},
    },
    "summary": "Retrieve a user's collection of illustrations",
    "tags": ["Collections"],
    "examples": [COLLECTION_RESPONSE_EXAMPLE],
}
