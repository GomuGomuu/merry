from django.db import transaction
from torch.fx.experimental.unification.unification_tools import first

from api.card.models import CardIllustration
from api.collection.models import Collection, CollectionIllustration

import logging

logger = logging.getLogger(__name__)


def add_illustration_to_collection(user, illustration_slug, collection_id=None):
    try:
        with transaction.atomic():
            if collection_id:
                collection = Collection.objects.get(id=collection_id)
            else:
                collection = Collection.objects.get(user=user, name="Vault")
            collection.collection_illustrations.create(
                illustration=CardIllustration.objects.get(code=illustration_slug)
            )
            logger.info(
                f"Illustration {illustration_slug} added to collection {collection.name}"
            )
    except Collection.DoesNotExist as exc:
        logger.error(f"Collection with id {collection_id} does not exist")
        raise exc


def remove_illustration_from_collection(user, illustration_slug, collection_id=None):
    try:
        with transaction.atomic():
            if collection_id:
                collection = Collection.objects.get(id=collection_id)
            else:
                collection = Collection.objects.get(user=user, name="Vault")
            connections = collection.collection_illustrations.filter(illustration__code=illustration_slug).first()
            logger.info(connections.delete())
            logger.info(connections)
            logger.info(
                f"Illustration {illustration_slug} removed from collection {collection.name}"
            )
    except Collection.DoesNotExist as exc:
        logger.error(f"Collection with id {collection_id} does not exist")
        raise exc


def get_collection_illustration(user, collection_id=None):
    collection = Collection.objects.get(user=user, id=collection_id or "Vault")
    return collection.illustrations.all()
