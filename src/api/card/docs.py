from rest_framework import status

from api.card.serializers.card import (
    CardSerializer,
    OpSerializer,
    DeckColorSerializer,
    ArtTypeSerializer,
    TypeSerializer,
    CrewSerializer,
)

card_tag = "Card Management"

card_list = {
    "request": CardSerializer,
    "responses": {status.HTTP_200_OK: CardSerializer(many=True)},
    "summary": "List all cards",
    "tags": [card_tag],
}

card_detail = {
    "request": CardSerializer,
    "responses": {status.HTTP_200_OK: CardSerializer},
    "summary": "Get card",
    "tags": [card_tag],
}

create_card = {
    "request": CardSerializer,
    "responses": {status.HTTP_201_CREATED: CardSerializer},
    "summary": "Create card",
    "tags": [card_tag],
}

update_card = {
    "request": CardSerializer,
    "responses": {status.HTTP_200_OK: CardSerializer},
    "summary": "Update card",
    "tags": [card_tag],
}

delete_card = {
    "request": CardSerializer,
    "responses": {status.HTTP_204_NO_CONTENT: None},
    "summary": "Delete card",
    "tags": [card_tag],
}

CARD_INFO_TAG = "Card Infos"

op_list = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: OpSerializer(many=True)},
    "summary": "List all ops",
    "tags": [CARD_INFO_TAG],
}

op_detail = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: OpSerializer},
    "summary": "Get op",
    "tags": [CARD_INFO_TAG],
}

deck_color_list = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: DeckColorSerializer(many=True)},
    "summary": "List all deck colors",
    "tags": [CARD_INFO_TAG],
}

deck_color_detail = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: DeckColorSerializer},
    "summary": "Get deck color",
    "tags": [CARD_INFO_TAG],
}

art_type_list = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: ArtTypeSerializer(many=True)},
    "summary": "List all art types",
    "tags": [CARD_INFO_TAG],
}

art_type_detail = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: ArtTypeSerializer},
    "summary": "Get art type",
    "tags": [CARD_INFO_TAG],
}

type_list = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: TypeSerializer(many=True)},
    "summary": "List all types",
    "tags": [CARD_INFO_TAG],
}

type_detail = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: TypeSerializer},
    "summary": "Get type",
    "tags": [CARD_INFO_TAG],
}

crew_list = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: CrewSerializer(many=True)},
    "summary": "List all crews",
    "tags": [CARD_INFO_TAG],
}

crew_detail = {
    "request": OpSerializer,
    "responses": {status.HTTP_200_OK: CrewSerializer},
    "summary": "Get crew",
    "tags": [CARD_INFO_TAG],
}
