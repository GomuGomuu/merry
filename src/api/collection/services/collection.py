from django.db import transaction

from api.collection.models import Collection

import logging

logger = logging.getLogger(__name__)


def add_illustration_to_collection(user, illustration_slug, collection_id=None):
    try:
        with transaction.atomic():
            if collection_id:
                collection = Collection.objects.get(id=collection_id)
            else:
                collection = Collection.objects.get(user=user, name="Vault")
            collection.illustrations.add(illustration_slug)
    except Collection.DoesNotExist as exc:
        logger.error(f"Collection with id {collection_id} does not exist")
        raise exc


def get_collection_illustration(user, collection_id=None):
    collection = Collection.objects.get(user=user, id=collection_id or "Vault")
    return collection.illustrations.all()
